from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import uuid7

from pydantic import UUID7
from sqlalchemy import Enum, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base
from src.transactions.enums import TransactionType

if TYPE_CHECKING:
    from src.receipts.model import ReceiptsOrm
    from src.users.model import UsersOrm


class TransactoinsOrm(Base):
    """All records of money flows"""

    id: Mapped[UUID7] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=lambda: uuid7(),
        comment="Unique identifier for the receipt",
    )
    owner_id: Mapped[UUID7] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
        comment="Reference to a user that owns this receipt registry",
    )
    receipt_id: Mapped[UUID7 | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("receipts.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        comment="Reference to fiscal receipt",
    )

    total: Mapped[Decimal] = mapped_column(
        Numeric(precision=15, scale=2),
        nullable=False,
        comment="Total amount for transaction",
    )
    type: Mapped[TransactionType] = mapped_column(
        Enum(
            TransactionType,
            native_enum=False,
            values_callable=lambda e: [m.value for m in e],
            validate_strings=True,
            create_constraint=True,
            name="type",
        ),
        nullable=False,
        index=True,
        comment="Transaction type by money flow",
    )

    # Relations
    owner: Mapped["UsersOrm"] = relationship(
        "UsersOrm",
        back_populates="receipts",
        lazy="selectin",
    )
    receipt: Mapped["ReceiptsOrm"] = relationship(
        "ReceiptsOrm",
        back_populates="transaction",
        lazy="selectin",
    )
