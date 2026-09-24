from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.operators.service import OperatorsService


def get_operators_service(db: AsyncSession = Depends(get_db)):
    return OperatorsService(db)
