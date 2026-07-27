from typing import AsyncGenerator
from uuid import uuid7

from sqlalchemy import JSON, Column, DateTime, String, func
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from src.config import settings

Base = declarative_base()

engine = create_async_engine(settings.database_url)
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


class ReceiptsOrm(Base):
    """Table of all receipts gathered from exteral API"""
    __tablename__ = "receipts_orm"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid7()))
    qr_code = Column(String, unique=True, index=True, nullable=False)
    receipt_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
