from urllib import parse

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class DatabaseSettings(BaseSettings):
    DB_USERNAME: str | None = None
    DB_PASSWORD: str | None = None
    DB_HOST: str | None = None
    DB_PORT: int | None = None
    DB_DATABASE: str | None = None
    DB_DRIVERNAME: str = 'mysql+aiomysql'

    @property
    def url(self) -> str:
        url = URL.create(
            drivername=self.DB_DRIVERNAME,
            username=self.DB_USERNAME,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_DATABASE,
        ).render_as_string(hide_password=False)
        return parse.unquote(url)

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='allow')


database_settings = DatabaseSettings()
