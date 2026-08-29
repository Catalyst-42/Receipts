from typing import Annotated

from fastapi import Depends, Path
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.core.schemes import ErrorResponse
from src.payments.schemes import PaymentId, Payment, PaymentList
from src.core.schemes import Count

from src.payments.service import PaymentsService

router = APIRouter(prefix="/payments", tags=["Payments"])


def get_payments_service(db: AsyncSession = Depends(get_db)):
    return PaymentsService(db)


@router.get("/", response_model=PaymentList)
async def get_payment_types(
    payments_service: PaymentsService = Depends(get_payments_service),
) -> PaymentList:
    """Returns all directory of payment types"""
    result = await payments_service.get_all()
    return result


@router.get(
    "/stats/count",
    response_model=Count,
)
async def get_receipts_count(
    payments_service: PaymentsService = Depends(get_payments_service),
) -> Count:
    """Returns total count of payment types in database"""
    return await payments_service.get_count()


@router.get(
    "/{payment_id}",
    response_model=Payment,
    responses={
        404: {"model": ErrorResponse, "description": "Payment type not found"},
    },
)
async def get_payment_type(
    request: Annotated[PaymentId, Path()],
    service: PaymentsService = Depends(get_payments_service),
) -> Payment:
    """Finds payment type by its id"""
    result = await service.get_by_id(request.payment_id)
    return result
