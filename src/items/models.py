from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID, uuid7

from sqlalchemy import Float, ForeignKey, Numeric, SmallInteger, String
from sqlalchemy.dialects.postgresql import UUID as SQL_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base

if TYPE_CHECKING:
    from src.receipts.models import ReceiptsOrm


class ItemsOrm(Base):
    """Table of all bought items from receipts one by one"""

    id: Mapped[UUID] = mapped_column(
        SQL_UUID(as_uuid=True),
        primary_key=True,
        index=True,
        unique=True,
        default=lambda: uuid7(),
        comment="Unique identifier for the item",
    )
    receipt_id: Mapped[UUID] = mapped_column(
        SQL_UUID(as_uuid=True),
        ForeignKey("receipts_orm.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
        comment="Relations to receipt with this item",
    )

    # Important
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        comment="Employee name",
    )
    price: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False, comment="Price for exactly one measure of item"
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
        ForeignKey("measures_orm.id", ondelete="RESTRICT"),
        nullable=False,
        comment="Type of measure for bought item",
    )
    nds: Mapped[int] = mapped_column(
        SmallInteger,
        ForeignKey("nds_orm.id", ondelete="RESTRICT"),
        nullable=False,
        comment="Type of VAT (НДС) for item",
    )
    payment: Mapped[int] = mapped_column(
        SmallInteger,
        ForeignKey("payments_orm.id", ondelete="RESTRICT"),
        nullable=False,
        comment="Item payment type",
    )
    product: Mapped[int] = mapped_column(
        SmallInteger,
        ForeignKey("products_orm.id", ondelete="RESTRICT"),
        nullable=False,
        comment="Product category",
    )

    # Relations
    receipt: Mapped["ReceiptsOrm"] = relationship(
        "ReceiptsOrm",
        back_populates="items",
    )
