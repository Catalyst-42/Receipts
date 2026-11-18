from pydantic import UUID7
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.transactional import transactional
from src.transactions.dao import TransactionsDao
from src.transactions.enums import TransactionType
from src.transactions.schemas import Transaction

from decimal import Decimal


class TransactionsService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.transactions_dao = TransactionsDao(db)

    @transactional
    async def create(self, owner_id: UUID7, receipt_id: UUID7, total: Decimal, type: TransactionType, note: str | None = None) -> Transaction:
        result = self.transactions_dao.create(
            owner_id=owner_id,
            receipt_id=receipt_id,
            total=total,
            type=type,
            note=note,
        )

        return Transaction.model_validate(result)
