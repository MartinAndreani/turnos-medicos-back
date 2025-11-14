from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_DATABASE: str

    @property
    def DATABASE_URL(self):
        return (f"postgresql+psycopg2://{self.DB_USERNAME}:{self.DB_PASSWORD}"
                f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}")

    class Config:
        env_file = ".env"

settings = Settings()
