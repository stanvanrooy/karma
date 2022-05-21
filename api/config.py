import configparser
import os
import dataclasses
from flask import Flask


@dataclasses.dataclass
class DatabaseConfig:
    uri: str


@dataclasses.dataclass
class Config:
    database: DatabaseConfig


def _load_config() -> Config:
    path = os.environ.get("KARMA_CONFIG", "config.ini")
    config = configparser.ConfigParser()
    config.read(path)

    database_config = DatabaseConfig(
        uri=config["database"]["uri"]
    )

    return Config(database_config)


def init_app(app: Flask):
    config = _load_config()
    app.config["SQLALCHEMY_DATABASE_URI"] = config.database.uri
