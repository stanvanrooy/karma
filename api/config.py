import configparser
import os
import dataclasses
from flask import Flask


@dataclasses.dataclass
class DatabaseConfig:
    uri: str


@dataclasses.dataclass
class AdminConfig:
    password: str


@dataclasses.dataclass
class Config:
    database: DatabaseConfig
    admin: AdminConfig


def _load_config() -> Config:
    path = os.environ.get("KARMA_CONFIG", "config.ini")
    config = configparser.ConfigParser()
    config.read(path)

    database_config = DatabaseConfig(
        uri=config["database"]["uri"]
    )

    admin_config = AdminConfig(
        password=config["admin"]["password"]
    )

    return Config(database_config, admin_config)


def init_app(app: Flask):
    config = _load_config()
    app.config["SQLALCHEMY_DATABASE_URI"] = config.database.uri


def get_config() -> Config:
    return _load_config()

