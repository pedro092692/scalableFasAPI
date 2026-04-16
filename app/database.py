from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import get_settings

settings = get_settings()


# connection engine
engine = create_engine(
    settings.database_url,
)

# the sessions factory for each request create a new session
LocalSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# base class for every models
class Base(DeclarativeBase):
    pass


# create db tables
def create_tables():
    Base.metadata.create_all(bind=engine)
