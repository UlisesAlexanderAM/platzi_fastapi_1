from pydantic import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pathlib import Path


base_dir = Path(__file__).resolve().parent.parent
DEFAULT_SQLITE_FILENAME = "movies.db"


class Settings(BaseSettings):
    sqlite_filename: str = DEFAULT_SQLITE_FILENAME
    sqlite_url: str = f"sqlite:///{base_dir.joinpath(sqlite_filename)}"

    class Config:
        case_sensitive = False
        env_file = ".env"


settings = Settings()
engine = create_engine(settings.sqlite_url, echo=True)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
