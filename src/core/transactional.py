import contextvars
from functools import wraps

from sqlalchemy.ext.asyncio import AsyncSession

_tx_active: contextvars.ContextVar[bool] = contextvars.ContextVar(
    "tx_active", default=False
)


def transactional(func):
    """Transactional pattern"""

    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        db: AsyncSession = getattr(self, "db", None)
        if db is None:
            raise AttributeError("Service has no 'db' attribute")

        if _tx_active.get():
            return await func(self, *args, **kwargs)

        token = _tx_active.set(True)
        try:
            result = await func(self, *args, **kwargs)
            await db.commit()
            return result
        except Exception:
            await db.rollback()
            raise
        finally:
            _tx_active.reset(token)

    return wrapper
