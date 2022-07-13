from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import Any

import httpx
from logdecorator import log_on_end, log_on_error, log_on_start
from pydantic import ValidationError

from config import Config, get_conf, logging
from handlers import NotificationHandler
from models import (EmailNotificationModel, NotificationModel,
                    PostNotificationModel, SMSNotificationModel)


@log_on_end(logging.INFO, "Dataset fetched")
def load_dataset(source_url: str) -> Any:
    response = httpx.get(url=source_url)

    if response.status_code == 200:
        return response.json()


@log_on_error(
    logging.ERROR, "{e!r}", on_exceptions=ValidationError, reraise=False
)  # noqa E501
def task(handler: NotificationHandler, notification: dict):

    basic_notification: NotificationModel = handler.handle(notification)

    handlers = NotificationHandler(EmailNotificationModel)
    handlers.set_next(NotificationHandler(PostNotificationModel)).set_next(
        NotificationHandler(SMSNotificationModel)
    )

    specific_notification: NotificationModel = handlers.handle(
        basic_notification.dict()
    )

    specific_notification.notify()


@log_on_start(logging.INFO, "STARTED")
@log_on_error(logging.ERROR, "{e!r}", on_exceptions=ValueError, reraise=False)
@log_on_end(logging.INFO, "FINISHED")
def execute(config: Config):
    dataset: Any = load_dataset(config.source_url)

    if not isinstance(dataset, list):
        raise ValueError("Incorrect dataset.")

    basic_handler: NotificationHandler = NotificationHandler(NotificationModel)

    handled_task = partial(task, basic_handler)

    with ThreadPoolExecutor(max_workers=config.max_workers) as executor:
        executor.map(handled_task, dataset)


if __name__ == "__main__":
    conf = get_conf("../conf-logs-volume/config.json")

    if conf is None:
        raise SystemExit("Invalid config.")

    execute(conf)
