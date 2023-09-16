import boto3


def create_page_table():
    dynamodb = boto3.resource('dynamodb',
                              region_name='us-east-1',
                              endpoint_url='http://dynamodb:4566',
                              aws_access_key_id='dummy12121',
                              aws_secret_access_key='dummy12121')

    table_name = 'Pages'
    key_schema = [
        {
            'AttributeName': 'page_id',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'page_name',
            'KeyType': 'RANGE'
        }
    ]
    attribute_definitions = [
        {
            'AttributeName': 'page_id',
            'AttributeType': 'N'
        },
        {
            'AttributeName': 'page_name',
            'AttributeType': 'S'
        },
    ]
    provisioned_throughput = {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }

    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=key_schema,
        AttributeDefinitions=attribute_definitions,
        ProvisionedThroughput=provisioned_throughput
    )

    table.wait_until_exists()
