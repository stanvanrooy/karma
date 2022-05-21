import configparser

from typing import Optional
import dataclasses
import enum


class DatabaseProvider(enum.Enum):
    SQLITE = "sqlite"


@dataclasses.dataclass
class DatabaseConfig:
    provider: DatabaseProvider
    path: Optional[str]


@dataclasses.dataclass
class Config:
    database: DatabaseConfig


def load_config(path: str) -> Config:
    config = configparser.ConfigParser()
    config.read(path)

    database_config = config["database"]
    database_provider = database_config["provider"]
    database_path = database_config.get("path", None)

    return Config(
        database=DatabaseConfig(
            provider=DatabaseProvider(database_provider),
            path=database_path,
        )
    )

