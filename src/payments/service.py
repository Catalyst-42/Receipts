from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.schemes import Count
from src.payments.dao import PaymentsDao
from src.payments.schemes import Payment, PaymentList


class PaymentsService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.payments_dao = PaymentsDao(db)

    async def get_all(self) -> PaymentList:
        result = await self.payments_dao.get_all()

        return PaymentList(items=[Payment.model_validate(item) for item in result])

    async def get_by_id(self, payment_id: int) -> Payment:
        result = await self.payments_dao.get_by_id(payment_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Payment type with id {payment_id} not found ",
            )

        return Payment.model_validate(result)

    async def get_count(self) -> Count:
        result = await self.payments_dao.get_count()
        return Count(total=result)
