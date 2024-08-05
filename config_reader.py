from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr
    db_host: SecretStr
    db_user: SecretStr
    db_password: SecretStr
    db_name: SecretStr
    telegram_group_id: SecretStr

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


config = Settings()

