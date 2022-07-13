import logging
import os
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, ValidationError

APP_PATH = Path(os.path.abspath(__file__)).parent
CONF_LOG_PATH = APP_PATH.parent.joinpath("conf-logs-volume")

logging.basicConfig(
    filename=f"{CONF_LOG_PATH}/redo.log",
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
    datefmt="%d.%m.%Y %H:%M:%S",
)


class Config(BaseModel):
    source_url: str
    max_workers: int = 5


def get_conf() -> Optional[Config]:
    try:
        return Config.parse_file(f"{CONF_LOG_PATH}/config.json")
    except ValidationError as errs:
        msg = ";".join([f'{err["loc"]} {err["msg"]}' for err in errs.errors()])
        logging.error(msg)
        return None
