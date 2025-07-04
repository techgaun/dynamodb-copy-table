#!/usr/bin/env python
import boto3
from botocore.exceptions import ClientError
from time import sleep
import sys
import os

if len(sys.argv) != 3:
    print("Usage: %s <source_table_name> <destination_table_name>" % sys.argv[0])
    sys.exit(1)

src_table = sys.argv[1]
dst_table = sys.argv[2]
default_region = os.getenv('AWS_DEFAULT_REGION', 'us-west-2')
src_region = os.getenv('AWS_SRC_REGION', default_region)
dst_region = os.getenv('AWS_dst_REGION', default_region)

src_resource = boto3.resource('dynamodb', region_name=src_region)
dst_resource = boto3.resource('dynamodb', region_name=dst_region)
dst_client = boto3.client('dynamodb', region_name=dst_region)

# 1. Read and copy the target table to be copied
try:
    logs = src_resource.Table(src_table)
    src_desc = logs.table_status  # Will raise if table doesn't exist
except Exception:
    print("Table %s does not exist" % src_table)
    sys.exit(1)

print("*** Reading key schema from %s table" % src_table)
src_table_desc = src_resource.meta.client.describe_table(TableName=src_table)['Table']
key_schema = src_table_desc['KeySchema']
attribute_definitions = src_table_desc['AttributeDefinitions']

hash_key = ''
range_key = ''
for schema in key_schema:
    attr_name = schema['AttributeName']
    key_type = schema['KeyType']
    if key_type == 'HASH':
        hash_key = attr_name
    elif key_type == 'RANGE':
        range_key = attr_name

# 2. Create the new table
try:
    dst_table_obj = dst_resource.Table(dst_table)
    dst_table_obj.load()
    if 'DISABLE_CREATION' in os.environ:
        print("Creation of new table is disabled. Skipping...")
    else:
        print("Table %s already exists" % dst_table)
        sys.exit(0)
except ClientError as e:
    if e.response['Error']['Code'] == 'ResourceNotFoundException':
        if 'DISABLE_CREATION' in os.environ:
            print("Creation of new table is disabled. Skipping...")
            sys.exit(0)
        # Use same key schema and attribute definitions as source
        params = {
            'TableName': dst_table,
            'KeySchema': key_schema,
            'AttributeDefinitions': attribute_definitions,
            'BillingMode': src_table_desc.get('BillingModeSummary', {}).get('BillingMode', 'PAY_PER_REQUEST')
        }
        if 'ProvisionedThroughput' in src_table_desc:
            params['ProvisionedThroughput'] = {
                'ReadCapacityUnits': src_table_desc['ProvisionedThroughput']['ReadCapacityUnits'],
                'WriteCapacityUnits': src_table_desc['ProvisionedThroughput']['WriteCapacityUnits']
            }
        dst_client.create_table(**params)
        print("*** Waiting for the new table %s to become active" % dst_table)
        waiter = dst_client.get_waiter('table_exists')
        waiter.wait(TableName=dst_table)
        # Wait until ACTIVE
        while dst_resource.Table(dst_table).table_status != 'ACTIVE':
            sleep(3)
        dst_table_obj = dst_resource.Table(dst_table)
    else:
        raise

if 'DISABLE_DATACOPY' in os.environ:
    print("Copying of data from source table is disabled. Exiting...")
    sys.exit(0)

# 3. Add the items
scan_kwargs = {}
done = False
start_key = None

while not done:
    if start_key:
        scan_kwargs['ExclusiveStartKey'] = start_key
    response = logs.scan(**scan_kwargs)
    items = response.get('Items', [])
    for item in items:
        new_item = {}
        new_item[hash_key] = item[hash_key]
        if range_key:
            new_item[range_key] = item[range_key]
        for f in item.keys():
            if f in [hash_key, range_key]:
                continue
            new_item[f] = item[f]
        try:
            dst_table_obj.put_item(Item=new_item)
        except ClientError as e:
            print(dst_table, new_item, e)
    start_key = response.get('LastEvaluatedKey', None)
    done = start_key is None

print("We are done. Exiting...")
