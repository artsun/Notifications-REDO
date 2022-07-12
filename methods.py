from time import sleep

import backoff


def send_email(email: str, data: dict) -> None:
    sleep(0.1)
    print(f"EMAIL sent to {email}. Data: {data}")


@backoff.on_exception(
    wait_gen=backoff.expo, exception=(ConnectionError,), max_tries=5, logger=None
)
def send_post(url: str, data: dict) -> None:
    sleep(0.1)
    print(f"POST sent to {url}. Data: {data}")


def send_sms(phone: str, data: dict) -> None:
    sleep(0.1)
    print(f"SMS sent to {phone}. Data: {data}")
