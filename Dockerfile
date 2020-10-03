FROM python:3.6-alpine
WORKDIR /project
COPY . /project
RUN pip install -r requirements.txt

CMD ["python","dynamodb-copy-table.py"]