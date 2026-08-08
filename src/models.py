from uuid import uuid7

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Numeric,
    SmallInteger,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID

from src.core.db import Base


class ReceiptsOrm(Base):
    """Table of all receipts gathered from external API"""

    __table_args__ = (UniqueConstraint("fn", "i", "fp"),)

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=lambda: uuid7(),
        unique=True,
        comment="Unique identifier for the receipt",
    )

    # Fiscal signs
    t = Column(
        DateTime,
        nullable=False,
        comment="Receipt timestamp",
    )
    s = Column(
        Numeric(precision=15, scale=2),
        nullable=False,
        comment="Total amount",
    )
    fn = Column(
        BigInteger,
        nullable=False,
        comment="Fiscal drive number (ФН)",
    )
    i = Column(
        BigInteger,
        nullable=False,
        comment="Fiscal document number (ФД)",
    )
    fp = Column(
        BigInteger,
        nullable=False,
        comment="Fiscal sign (ФП)",
    )
    n = Column(
        SmallInteger,
        nullable=False,
        comment="Operation type",
    )

    # CRPT answer
    crpt_data = Column(
        JSONB,
        nullable=False,
        comment="Full receipt data in JSON format from CRPT API",
    )
