from concurrent.futures import ThreadPoolExecutor
from typing import List

from httpx import Request
from pydantic import parse_file_as

from config import get_conf
from handlers import NotificationHandler
from models import (
    EmailNotificationModel,
    NotificationModel,
    PostNotificationModel,
    SMSNotificationModel,
)


def task(notification: NotificationModel):
    handlers = NotificationHandler(EmailNotificationModel)
    handlers.set_next(NotificationHandler(PostNotificationModel)).set_next(
        NotificationHandler(SMSNotificationModel)
    )
    handlers.handle(notification)


if __name__ == "__main__":
    print("START")
    conf = get_conf("config.json")
    notifications: List[NotificationModel] = parse_file_as(
        List[NotificationModel], conf.source_url
    )

    with ThreadPoolExecutor(max_workers=conf.max_workers) as executor:
        executor.map(task, notifications)

    print(len(notifications))
