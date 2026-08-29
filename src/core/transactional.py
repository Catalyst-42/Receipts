from functools import wraps

from sqlalchemy.ext.asyncio import AsyncSession


def transactional(func):
    """Transactional pattern"""

    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        db: AsyncSession = getattr(self, "db", None)
        if db is None:
            raise AttributeError(
                f"Service {self.__class__.__name__} must have 'db' attribute"
            )

        if db.in_transaction():
            return await func(self, *args, **kwargs)

        async with db.begin():
            return await func(self, *args, **kwargs)

    return wrapper
