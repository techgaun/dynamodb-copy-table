# dynamodb-copy-table-python3
A simple python 3 script to copy dynamodb table

---

### Requirements

- Python 3.x
- boto (`pip install boto`)

### Usage

A simple usage example:

```shell
$ python dynamodb-copy-table.py src_table dst_table
```

The following environment variables can be used:
Variable | Purpose
--- | ---
`AWS_DEFAULT_REGION` | Select the region (the default region is `us-west-2`)
`DISABLE_CREATION` | Disable the creation of a new table (Useful if the table already exists)
`DISABLE_DATACOPY` | Disable the copying of data from source table to destination table

```shell
$ AWS_DEFAULT_REGION=us-east-1 DISABLE_CREATION=yes DISABLE_DATACOPY=yes \
python dynamodb-copy-table.py src_table dst_table
```

### References

- [Import and Export DynamoDB Data using AWS Data Pipeline](http://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/dp-importexport-ddb.html)
