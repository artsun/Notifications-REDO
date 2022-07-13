from random import getrandbits
from time import sleep

import backoff
from logdecorator import log_on_end

from config import logging


@log_on_end(logging.INFO, "EMAIL sent to {email!s}")
def send_email(email: str, data: dict) -> None:
    """Mock."""
    sleep(0.1)
    print(f"EMAIL sent to {email}. Data: {data}")


@log_on_end(logging.INFO, "POST sent to {url!s}")
@backoff.on_exception(
    wait_gen=backoff.expo,
    exception=(ConnectionError,),
    max_tries=5,
    logger=logging.getLogger(),
)
def send_post(url: str, data: dict) -> None:
    """Mock function imitates unstable connection."""
    sleep(0.1)
    if getrandbits(1):
        raise ConnectionError("Connection failed")
    print(f"POST sent to {url}. Data: {data}")


@log_on_end(logging.INFO, "SMS sent to {phone!s}")
def send_sms(phone: str, data: dict) -> None:
    """Mock."""
    sleep(0.1)
    print(f"SMS sent to {phone}. Data: {data}")
