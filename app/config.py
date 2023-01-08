from pydantic import BaseSettings

class Settings(BaseSettings):
   database_hostname: str = "localhost"
   database_port: str = "5432"
   database_password: str = "surgeon"
   database_name: str = "fastapi"
   database_username: str = "postgres"
   secrey_key: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
   algorithm: str 
   access_token_expire_minutes: int = 30

   class config:
        env_file = ".env"

   #Settings = Settings()   