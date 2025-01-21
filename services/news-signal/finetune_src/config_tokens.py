from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigTokens(BaseSettings):
    model_config = SettingsConfigDict(env_file='tokens.env')

    COMET_API_KEY: str
    HF_TOKEN: str

config = ConfigTokens()
