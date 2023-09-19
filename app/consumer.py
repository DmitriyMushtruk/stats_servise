import os
import pika
import sys
import json
from config import settings
from database import (
    create_or_delete_page,
    add_or_remove_post,
    add_or_remove_follower,
    add_or_remove_like,
    add_comment_or_repost
)


def main():
    connection = pika.BlockingConnection(
        pika.URLParameters(settings.BROKER_URL))
    channel = connection.channel()

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

        message_data = json.loads(body.decode("utf-8"))
        page_id = message_data[1]["body"]["page_id"]
        action = message_data[1]["body"]["action"]

        if action in ["page_created", "page_deleted"]:
            create_or_delete_page(page_id, action)
        elif action in ["post_created", "post_deleted"]:
            add_or_remove_post(page_id, action)
        elif action in ["add_follower", "remove_follower"]:
            add_or_remove_follower(page_id, action)
        elif action in ["add_like", "remove_like"]:
            add_or_remove_like(page_id, action)
        elif action in ["add_comment", "add_repost"]:
            add_comment_or_repost(page_id, action)

    channel.basic_consume(queue='stats', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
