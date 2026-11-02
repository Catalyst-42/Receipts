from pydantic import UUID7
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.transactional import transactional
from src.transactions.dao import TransactionsDao
from src.transactions.schemas import Transaction


class TransactionsService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.transactions_dao = TransactionsDao(db)

    @transactional
    async def create(self) -> Transaction:
        pass