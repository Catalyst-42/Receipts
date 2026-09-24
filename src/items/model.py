from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import uuid7

from pydantic import UUID7
from sqlalchemy import Float, ForeignKey, Numeric, SmallInteger, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base

if TYPE_CHECKING:
    from src.receipts.model import ReceiptsOrm


class ItemsOrm(Base):
    """Table of all bought items from receipts one by one"""

    id: Mapped[UUID7] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=lambda: uuid7(),
        comment="Unique identifier for the item",
    )
    receipt_id: Mapped[UUID7] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("receipts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Relations to receipt with this item",
    )

    # Important
    name: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
        comment="Item name",
    )
    price: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False,
        comment="Price for exactly one measure of item",
    )

    # Receipt item specific
    total: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False,
        comment="Total price of items bought, should be equal to quantity times price",
    )
    quantity: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Number of items bought",
    )

    # Linked directories
    measure: Mapped[int] = mapped_column(
        SmallInteger,
        ForeignKey("measures.id", ondelete="RESTRICT"),
        index=True,
        nullable=False,
        comment="Type of measure for bought item",
    )
    nds: Mapped[int] = mapped_column(
        SmallInteger,
        ForeignKey("nds.id", ondelete="RESTRICT"),
        index=True,
        nullable=False,
        comment="Type of VAT (НДС) for item",
    )
    payment: Mapped[int] = mapped_column(
        SmallInteger,
        ForeignKey("payments.id", ondelete="RESTRICT"),
        index=True,
        nullable=False,
        comment="Item payment type",
    )
    product: Mapped[int] = mapped_column(
        SmallInteger,
        ForeignKey("products.id", ondelete="RESTRICT"),
        index=True,
        nullable=False,
        comment="Product category",
    )

    # Relations
    receipt: Mapped["ReceiptsOrm"] = relationship(
        "ReceiptsOrm",
        back_populates="items",
        lazy="selectin",
    )
