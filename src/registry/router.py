from typing import Annotated

from fastapi import Depends, Query, Path
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.core.schemes import ErrorResponse
from src.receipts.schemes import FiscalFields, ReceiptId
from src.registry.schemes import Registry
from src.registry.service import RegistryService

router = APIRouter(prefix="/registry", tags=["Registry"])


def get_registry_service(db: AsyncSession = Depends(get_db)):
    return RegistryService(db)


@router.post(
    "/by-fiscal-fields",
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
    "/by-fiscal-fields",
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


@router.get(
    "/by-fiscal-fields",
    response_model=Registry,
    responses={
        404: {"model": ErrorResponse, "description": "Registry not found"},
    },
)
async def get_registry_by_fiscal_fields(
    request: Annotated[FiscalFields, Query()],
    service: RegistryService = Depends(get_registry_service),
) -> Registry:
    """Returns registry of a receipt found by fiscal fields"""
    return await service.get(request)


@router.get(
    "/{receipt_id}",
    response_model=Registry,
    responses={
        404: {"model": ErrorResponse, "description": "Registry not found"},
    },
)
async def get_registry_by_receipt_id(
    request: Annotated[ReceiptId, Path()],
    service: RegistryService = Depends(get_registry_service),
) -> Registry:
    """Returns registry of a receipts found by receipt id"""
    return await service.get_by_receipt_id(request.receipt_id)
