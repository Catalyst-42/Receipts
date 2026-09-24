import re
from typing import AsyncGenerator

from sqlalchemy import MetaData, Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, declared_attr

from src.config import settings
from src.core.schemes import Count


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Make tablename from class name"""
        name = re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()
        name = name.removesuffix("_orm")
        return name


# Session
engine = create_async_engine(settings.database_url)
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Returns database session"""
    async with AsyncSessionLocal() as session:
        yield session


async def count_by_query(db: AsyncSession, stmt: Select) -> Count:
    """Returns count by query"""
    stmt = select(func.count()).select_from(stmt.subquery())
    return await db.scalar(stmt)
