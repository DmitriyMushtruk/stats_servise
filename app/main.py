import boto3
from fastapi import FastAPI, HTTPException
from pynamodb.connection import Connection
from app.config import settings


dynamodb = boto3.resource('dynamodb',
                          region_name=settings.REGION_NAME,
                          endpoint_url=settings.ENDPOINT_URL,
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

connection = Connection(dynamodb)

app = FastAPI()

table_names = dynamodb.meta.client.list_tables()['TableNames']

print(f"Number of tables found: {len(table_names)}")

for table_name in table_names:
    print(f"Table Name: {table_name}")


@app.get("/stats/")
async def get_page_stats(page_id: int):
    try:
        table = dynamodb.Table('Pages')
        response = table.get_item(
            Key={
                'page_id': page_id,
            }
        )

        if 'Item' in response:
            item = response['Item']
            return item
        else:
            raise HTTPException(status_code=404, detail="Page not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving data: {str(e)}")

