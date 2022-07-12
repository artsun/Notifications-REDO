import logging

logging.basicConfig(
    filename="redo.log",
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
    datefmt="%d.%m.%Y %H:%M:%S",
)
