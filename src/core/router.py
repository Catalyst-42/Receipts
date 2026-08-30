from datetime import datetime

from fastapi import Depends
from fastapi.responses import FileResponse
from fastapi.routing import APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.core.schemes import Status

router = APIRouter(tags=["Core"])


@router.get("/", include_in_schema=False)
async def root() -> FileResponse:
    """Returns a frontend page with receipt scanner"""
    return FileResponse("static/index.html")

@router.get("/status", include_in_schema=False)
async def get_health(
    db: AsyncSession = Depends(get_db),
) -> Status:
    """Returns status of an Receipts API"""
    try:
        result = await db.execute(select(True))
        database = result.scalar()
    except Exception:
        database = False

    return Status(
        system=True,
        database=database,
        timestamp=datetime.now(),
    )
