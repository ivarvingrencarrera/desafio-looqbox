from enum import StrEnum

from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvironmentEnum(StrEnum):
    PRODUCTION = 'production'
    TESTING = 'testing'
    DEVELOPMENT = 'development'


class GlobalSettings(BaseSettings):
    NAME: str = 'My Application'
    DESCRIPTION: str = 'This is a sample application.'
    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.DEVELOPMENT

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='allow')


global_settings = GlobalSettings()
