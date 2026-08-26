from typing import Annotated

from fastapi import Depends, Query
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.core.schemes import ErrorResponse
from src.receipts.schemes import FiscalFields
from src.registry.schemes import Registry
from src.registry.service import RegistryService

router = APIRouter(prefix="/registry", tags=["Registry"])


def get_registry_service(db: AsyncSession = Depends(get_db)):
    return RegistryService(db)


@router.post(
    "",
    response_model=Registry,
    responses={
        503: {"model": ErrorResponse, "description": "CRPT API not available"},
    },
)
async def create_registry(
    request: Annotated[FiscalFields, Query()],
    service: RegistryService = Depends(get_registry_service),
) -> Registry:
    """Registers receipt in project database"""
    return await service.create(request)


@router.delete(
    "",
    response_model=Registry,
    responses={
        404: {"model": ErrorResponse, "description": "Registry not found"},
    },
)
async def delete_registry(
    request: Annotated[FiscalFields, Query()],
    service: RegistryService = Depends(get_registry_service),
) -> Registry:
    """Deletes records of a registry"""
    return await service.delete(request)
