# dynamodb-copy-table
A simple python script to copy dynamodb table

---

### Requirements

- Python 2.x
- boto (`pip install boto`)

### Usage

A simple usage example:

```shell
$ python dynamodb-copy-table.py src_table dst_table
```

You can use the environment variables `AWS_DEFAULT_REGION` and `DISABLE_DATACOPY` to select the region (the default region is `us-west-2`) and disable the copying of data from source table to destination table.

```shell
$ AWS_DEFAULT_REGION=us-east-1 DISABLE_DATACOPY=yes python dynamodb-copy-table.py src_table dst_table
```

### References

- [Import and Export DynamoDB Data using AWS Data Pipeline](http://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/dp-importexport-ddb.html)
- [Original script](https://gist.github.com/iomz/9774415) - had to modify and add support for tables with only hash key
