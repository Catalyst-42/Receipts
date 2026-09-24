from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.items.service import ItemsService


def get_items_service(db: AsyncSession = Depends(get_db)):
    return ItemsService(db)
