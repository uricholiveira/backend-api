from typing import Generator

from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declared_attr, sessionmaker

from app.core.settings import settings

SQLALCHEMY_DATABASE_URL = settings.database.url

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={},
)
SessionLocal = sessionmaker(
    autocommit=settings.database.params.auto_commit,
    autoflush=settings.database.params.auto_flush,
    bind=engine,
)


def get_session() -> Generator:
    db = SessionLocal()
    try:
        db.begin()
        yield db
    finally:
        db.close()


@as_declarative()
class Base:
    id: str = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.replace("Model", "")
