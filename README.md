# dynamodb-copy-table-python3
A simple python 3 script to copy dynamodb table

---

### Requirements

- Python 3.x
- boto3 (`pip install boto3`)

### Usage

A simple usage example:

```shell
$ python dynamodb-copy-table.py src_table dst_table
```

The following environment variables can be used:
Variable | Purpose
--- | ---
`AWS_DEFAULT_REGION` | Select the region (the default region is `us-west-2`)
`AWS_SRC_REGION` | Select the source table region (the default region is AWS_DEFAULT_REGION)
`AWS_DST_REGION` | Select the destination table region (the default region is AWS_DEFAULT_REGION)
`DISABLE_CREATION` | Disable the creation of a new table (Useful if the table already exists)
`DISABLE_DATACOPY` | Disable the copying of data from source table to destination table

```shell
$ AWS_DEFAULT_REGION=us-east-1 DISABLE_CREATION=yes DISABLE_DATACOPY=yes \
python dynamodb-copy-table.py src_table dst_table
```

#### Docker Image

The docker image is available as [techgaun/dynamodb-copy-table:latest](https://hub.docker.com/r/techgaun/dynamodb-copy-table)
in the official docker hub that you can pull from.

Usage:

```shell
# pull image down
docker pull techgaun/dynamodb-copy-table:latest

# invoke help
$ docker run --rm -it techgaun/dynamodb-copy-table:latest
Usage: dynamodb-copy-table.py <source_table_name> <destination_table_name>

# invoke copy
docker run -e AWS_ACCESS_KEY_ID=abc -e AWS_SECRET_ACCESS_KEY=def --rm -it techgaun/dynamodb-copy-table:latest src dest
```

### References

- [Import and Export DynamoDB Data using AWS Data Pipeline](http://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/dp-importexport-ddb.html)
