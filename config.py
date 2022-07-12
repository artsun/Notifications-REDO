from typing import Optional

from pydantic import BaseModel, ValidationError

from logger import logging


class Config(BaseModel):
    source_url: str
    max_workers: int = 5


def get_conf(file_path: str) -> Optional[Config]:
    try:
        return Config.parse_file(file_path)
    except ValidationError as errs:
        msg = ";".join([f'{err["loc"]} {err["msg"]}' for err in errs.errors()])
        logging.error(msg)
        return None
