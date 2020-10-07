FROM python:3.6-alpine

LABEL maintainer="github.com/techgaun"
LABEL org.opencontainers.image.authors="kiddo3,techgaun"
LABEL org.opencontainers.image.title="DynamoDB Copy Table"
LABEL org.opencontainers.image.url="https://github.com/techgaun/dynamodb-copy-table"
LABEL org.opencontainers.image.documentation="https://github.com/techgaun/dynamodb-copy-table#readme"
LABEL org.opencontainers.image.source="https://github.com/techgaun/dynamodb-copy-table"

WORKDIR /project
COPY . /project
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "dynamodb-copy-table.py"]
