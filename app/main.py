import boto3
from fastapi import FastAPI, HTTPException
from pynamodb.connection import Connection


from app.database import create_page_table
from pynamodb.exceptions import TableError

# Написать логику добавления записей в таблицу
# Настроить логику изменения атрибутов followers likes и тд.
# Соответсвенно добавлять записи если страница создалась и удалять если страница удалилась
#
# ...

dynamodb = boto3.resource('dynamodb',
                          region_name='us-east-1',
                          endpoint_url='http://dynamodb:4566',
                          aws_access_key_id='dummy12121',
                          aws_secret_access_key='dummy12121')

connection = Connection(dynamodb)

app = FastAPI()

# create_page_table()
#
# table_name = 'Pages'
# table = dynamodb.Table(table_name)
#
# if table.table_status == 'ACTIVE':
#     print(f"Таблица '{table_name}' успешно создана.")
# else:
#     print("Не удалось создать таблицу.")
#
#
# table.put_item(
#     Item={
#         'page_id': 1,
#         'page_name': 'ExamplePage',
#         'followers': 1000,
#         'likes': 500,
#         'posts': 50,
#         'reposts': 20,
#         'comments': 100
#     }
# )


table_name = 'Pages'
table = dynamodb.Table(table_name)

response = table.get_item(
    Key={
        'page_id': 1,
        'page_name': 'ExamplePage'
    }
)

item = response['Item']
print(item)


@app.get("/stats/")
async def get_page_stats(page_id: int, page_name: str):
    try:
        response = table.get_item(
            Key={
                'page_id': page_id,
                'page_name': page_name
            }
        )

        if 'Item' in response:
            item = response['Item']
            return item  # Верните запись в виде JSON-ответа
        else:
            raise HTTPException(status_code=404, detail="Page not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving data: {str(e)}")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
