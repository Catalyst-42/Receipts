from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid7

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Numeric,
    SmallInteger,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID as SQL_UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.core.db import Base


class ReceiptsOrm(Base):
    """Table of all receipts gathered from external API"""

    __table_args__ = (UniqueConstraint("t", "s", "fn", "i", "fp", "n"),)

    id: Mapped[UUID] = mapped_column(
        SQL_UUID(as_uuid=True),
        primary_key=True,
        index=True,
        unique=True,
        default=lambda: uuid7(),
        comment="Unique identifier for the receipt",
    )
    crpt_id: Mapped[UUID] = mapped_column(
        SQL_UUID(as_uuid=True),
        ForeignKey("crpt_orm.id", ondelete="CASCADE"),
        nullable=False,
        comment="Reference to original CRPT data",
    )

    # Foreign key to CRPT model
    crpt_id: Mapped[UUID | None] = mapped_column(
        SQL_UUID(as_uuid=True),
        ForeignKey("crpt_orm.id", ondelete="CASCADE"),
        nullable=True,
        comment="Reference to the original CRPT record",
    )

    t: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        comment="Receipt timestamp",
    )
    s: Mapped[Decimal] = mapped_column(
        Numeric(precision=15, scale=2),
        nullable=False,
        comment="Total amount",
    )
    fn: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        comment="Fiscal drive number (ФН)",
    )
    i: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        comment="Fiscal document number (ФД)",
    )
    fp: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        comment="Fiscal sign (ФП)",
    )
    n: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
        comment="Operation type",
    )
