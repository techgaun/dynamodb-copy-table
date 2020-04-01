#!/usr/bin/env python
from boto.dynamodb2.exceptions import ValidationException
from boto.dynamodb2.fields import HashKey, RangeKey
from boto.dynamodb2.layer1 import DynamoDBConnection
from boto.dynamodb2.table import Table
from boto.exception import JSONResponseError
from time import sleep
import sys
import os

if len(sys.argv) != 3:
    print("Usage: %s <source_table_name> <destination_table_name>"% sys.argv[0])
    sys.exit(1)

src_table = sys.argv[1]
dst_table = sys.argv[2]
region = os.getenv('AWS_DEFAULT_REGION', 'us-west-2')

# host = 'dynamodb.%s.amazonaws.com' % region
# ddbc = DynamoDBConnection(is_secure=False, region=region, host=host)
DynamoDBConnection.DefaultRegionName = region
ddbc = DynamoDBConnection()

# 1. Read and copy the target table to be copied
table_struct = None
try:
    logs = Table(src_table, connection=ddbc)
    table_struct = logs.describe()
except JSONResponseError:
    print("Table %s does not exist" % src_table) 
    sys.exit(1)

print("*** Reading key schema from %s table" % src_table)
src = ddbc.describe_table(src_table)['Table']
hash_key = ''
range_key = ''
for schema in src['KeySchema']:
    attr_name = schema['AttributeName']
    key_type = schema['KeyType']
    if key_type == 'HASH':
        hash_key = attr_name
    elif key_type == 'RANGE':
        range_key = attr_name

# 2. Create the new table
table_struct = None
try:
    new_logs = Table(dst_table,
                    connection=ddbc,
                    schema=[HashKey(hash_key),
                            RangeKey(range_key),
                            ]
                    )

    table_struct = new_logs.describe()
    if 'DISABLE_CREATION' in os.environ:
        print("Creation of new table is disabled. Skipping...")
    else:
        print("Table %s already exists" % dst_table)
        sys.exit(0)
except JSONResponseError:
    schema = [HashKey(hash_key)]
    if range_key != '':
        schema.append(RangeKey(range_key))
    new_logs = Table.create(dst_table,
                            connection=ddbc,
                            schema=schema,
                            )
    print("*** Waiting for the new table %s to become active" % dst_table)
    sleep(5)
    while ddbc.describe_table(dst_table)['Table']['TableStatus'] != 'ACTIVE':
        sleep(3)
    

if 'DISABLE_DATACOPY' in os.environ:
    print("Copying of data from source table is disabled. Exiting...")
    sys.exit(0)

# 3. Add the items
for item in logs.scan():
    new_item = {}
    new_item[hash_key] = item[hash_key]
    if range_key != '':
        new_item[range_key] = item[range_key]
    for f in item.keys():
        if f in [hash_key, range_key]:
            continue
        new_item[f] = item[f]
    try:
        new_logs.use_boolean()
        new_logs.put_item(new_item, overwrite=True)
    except ValidationException:
        print(dst_table, new_item)
    except JSONResponseError:
        print(ddbc.describe_table(dst_table)['Table']['TableStatus'])

print("We are done. Exiting...")
