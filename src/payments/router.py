from typing import Annotated

from fastapi import Depends, Path
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.core.schemes import ErrorResponse
from src.payments.schemes import GetPaymentByIdRequest, Payment, PaymentList

from src.payments.service import PaymentsService

router = APIRouter(prefix="/payments", tags=["Payment types"])


def get_measures_service(db: AsyncSession = Depends(get_db)):
    return PaymentsService(db)


@router.get("/", response_model=PaymentList)
async def get_payment_types(
    service: PaymentsService = Depends(get_measures_service),
) -> PaymentList:
    """Returns all directory of payment types"""
    result = await service.get_all()
    return result


@router.get(
    "/{payment_id}",
    response_model=Payment,
    responses={
        404: {"model": ErrorResponse, "description": "Payment type not found"},
    },
)
async def get_payment_type(
    request: Annotated[GetPaymentByIdRequest, Path()],
    service: PaymentsService = Depends(get_measures_service),
) -> Payment:
    """Finds payment type by its id"""
    result = await service.get_by_id(request.payment_id)
    return result
