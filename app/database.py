import boto3
from config import settings


def get_table(table_name):
    dynamodb = boto3.resource('dynamodb',
                              region_name=settings.REGION_NAME,
                              endpoint_url=settings.ENDPOINT_URL,
                              aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

    table = dynamodb.Table(table_name)

    return table


def create_or_delete_page(page_id, action):
    table = get_table('Pages')

    if action == "page_created":
        table.put_item(
            Item={
                'page_id': page_id,
                'followers': 0,
                'likes': 0,
                'posts': 0,
                'reposts': 0,
                'comments': 0
            }
        )
        print("[*] Page ", page_id, "created in table")
    else:
        table.delete_item(
            Key={
                'page_id': page_id
            }
        )
        print("[*] Page", page_id, "deleted from table")


def attribute_increment(page_id, attr):
    table = get_table('Pages')
    table.update_item(
        Key={
            'page_id': page_id
        },
        UpdateExpression=f"SET {attr} = {attr} + :increment",
        ExpressionAttributeValues={
            ':increment': 1
        }
    )
    print(f"[*] Attribute {attr} increased by 1 for Page {page_id}")


def attribute_decrement(page_id, attr):
    table = get_table('Pages')
    table.update_item(
        Key={
            'page_id': page_id
        },
        UpdateExpression=f"SET {attr} = {attr} - :decrement",
        ExpressionAttributeValues={
            ':decrement': 1
        }
    )
    print(f"[*] Attribute {attr} decreased by 1 for Page {page_id}")


def add_or_remove_post(page_id, action):
    attr = "posts"
    if action == "post_created":
        attribute_increment(page_id, attr)
    else:
        attribute_decrement(page_id, attr)


def add_or_remove_follower(page_id, action):
    attr = "followers"
    if action == "add_follower":
        attribute_increment(page_id, attr)
    else:
        attribute_decrement(page_id, attr)


def add_or_remove_like(page_id, action):
    attr = "likes"
    if action == "add_like":
        attribute_increment(page_id, attr)
    else:
        attribute_decrement(page_id, attr)


def add_comment_or_repost(page_id, action):
    if action == "add_comment":
        attr = action
    else:
        attr = action

    attribute_increment(page_id, attr)
