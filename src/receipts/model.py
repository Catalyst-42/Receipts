from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import uuid7

from pydantic import UUID7
from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Numeric,
    SmallInteger,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID as SQL_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base

if TYPE_CHECKING:
    from src.crpt.models import CrptOrm
    from src.items.model import ItemsOrm
    from src.shops.model import RetailersOrm


class ReceiptsOrm(Base):
    """Table of all receipts gathered from external API"""

    __table_args__ = (UniqueConstraint("t", "s", "fn", "i", "fp", "n"),)

    id: Mapped[UUID7] = mapped_column(
        SQL_UUID(as_uuid=True),
        primary_key=True,
        index=True,
        unique=True,
        default=lambda: uuid7(),
        comment="Unique identifier for the receipt",
    )
    crpt_id: Mapped[UUID7] = mapped_column(
        SQL_UUID(as_uuid=True),
        ForeignKey("crpt_orm.id", ondelete="RESTRICT"),
        index=True,
        unique=True,
        nullable=False,
        comment="Reference to original CRPT data",
    )
    shop_id: Mapped[UUID7] = mapped_column(
        SQL_UUID(as_uuid=True),
        ForeignKey("shops_orm.id", ondelete="RESTRICT"),
        index=True,
        nullable=False,
        comment="Reference to shop, where receipt was made",
    )

    # Fiscal fields
    t: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        comment="Receipt timestamp",
    )
    s: Mapped[Decimal] = mapped_column(
        Numeric(precision=15, scale=2),
        nullable=False,
        comment="Sum of prices by items in receipt",
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

    # Relations
    crpt: Mapped["CrptOrm"] = relationship(
        "CrptOrm",
        back_populates="receipt",
        lazy="selectin",
    )
    shop: Mapped["RetailersOrm"] = relationship(
        "ShopsOrm",
        back_populates="receipt",
        lazy="selectin",
    )
    items: Mapped[list["ItemsOrm"]] = relationship(
        "ItemsOrm",
        back_populates="receipt",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
