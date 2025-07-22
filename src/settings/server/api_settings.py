from src.settings.globals import EnvironmentEnum, global_settings


class APISettings:
    @property
    def debug(self) -> bool:
        return global_settings.ENVIRONMENT != EnvironmentEnum.PRODUCTION

    @property
    def title(self) -> str:
        return global_settings.NAME

    @property
    def description(self) -> str:
        return global_settings.DESCRIPTION


api_settings = APISettings()
