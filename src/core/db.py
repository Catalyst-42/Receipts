from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, declared_attr
import re

from src.config import settings


class Base(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Make tablename from class name"""
        return re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()


# Session
engine = create_async_engine(settings.database_url)
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Returns database session"""
    async with AsyncSessionLocal() as session:
        yield session
