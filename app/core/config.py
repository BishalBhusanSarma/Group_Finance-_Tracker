from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME : str
    DEBUG : bool
    ACCESS_TOKEN_EXPIRY:int
    REFRESH_TOKEN_EXPIRY:int
    ALGORITHM:str
    SECRET_KEY:str
    DATABASE_URL:str
    

    model_config = SettingsConfigDict(env_file=".env",extra="ignore")

settings = Settings()