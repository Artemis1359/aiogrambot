import os

from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    TOKEN: str
    ADMIN_ID: int

    model_config = SettingsConfigDict(
        env_file=(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')),
        extra="ignore")

    def get_db_url(self):
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")

    def get_db_sync_url(self):
        return (f"postgresql://{self.DB_USER}:{self.DB_PASS}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")

settings = Settings()

# print(settings.get_db_url())
