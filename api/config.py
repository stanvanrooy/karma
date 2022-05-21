import configparser
import os

from typing import Optional
import dataclasses
import enum


class DatabaseProvider(enum.Enum):
    SQLITE = "sqllite"


@dataclasses.dataclass
class DatabaseConfig:
    provider: DatabaseProvider
    path: Optional[str]


@dataclasses.dataclass
class Config:
    database: DatabaseConfig


def _load_config() -> Config:
    path = os.environ.get("KARMA_CONFIG", "config.ini")
    config = configparser.ConfigParser()
    config.read(path)

    database_provider = config["database"]["provider"]
    database_path = config["database"]["path"]

    database_config = DatabaseConfig(
        provider=DatabaseProvider(database_provider),
        path=database_path
    )
    return Config(database_config)


__CONFIG = None
def get_config() -> Config:
    global __CONFIG
    if __CONFIG is None:
        __CONFIG = _load_config()
    return __CONFIG

