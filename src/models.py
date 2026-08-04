from uuid import uuid7
from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, func, Numeric, SmallInteger, String
from sqlalchemy.dialects.postgresql import JSONB, UUID

from src.core.db import Base


class ReceiptsOrm(Base):
    """Table of all receipts gathered from external API"""

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=lambda: uuid7(),
        comment="Unique identifier for the receipt",
    )
    qr_code = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
        comment="QR code content for the receipt",
    )
    receipt_data = Column(
        JSONB,
        nullable=False,
        comment="Full receipt data in JSON format",
    )
    created_at = Column(
        DateTime,
        server_default=func.now(),
        comment="Timestamp when the receipt was created",
    )

    # Fiscal signs
    t = Column(
        DateTime,
        nullable=True,
        comment="Receipt timestamp",
    )
    s = Column(
        Numeric(precision=15, scale=2),
        nullable=True,
        comment="Total amount",
    )
    fn = Column(
        BigInteger,
        nullable=True,
        comment="Fiscal drive number (ФН)",
    )
    i = Column(
        BigInteger,
        nullable=True,
        comment="Fiscal document number (номер чека)",
    )
    fp = Column(
        BigInteger,
        nullable=True,
        comment="Fiscal sign (ФП)",
    )
    n = Column(
        SmallInteger,
        nullable=True,
        comment="Operation type",
    )
