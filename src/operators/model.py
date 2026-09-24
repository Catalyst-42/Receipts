from typing import TYPE_CHECKING
from uuid import uuid7

from pydantic import UUID7
from sqlalchemy import ForeignKey, Index, String, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base

if TYPE_CHECKING:
    from src.receipts.model import ReceiptsOrm
    from src.retailers.model import RetailersOrm
    from src.shops.model import ShopsOrm


class OperatorsOrm(Base):
    """Table of all employess by shops"""

    __table_args__ = (
        UniqueConstraint("shop_id", "name"),
        Index(
            "ix_operators_retailer_name_null_shop",
            "retailer_id",
            "name",
            unique=True,
            postgresql_where=text("shop_id IS NULL"),
        ),
    )

    id: Mapped[UUID7] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=lambda: uuid7(),
        comment="Unique identifier for the operator",
    )
    retailer_id: Mapped[UUID7] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("retailers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Foreign key to retailers table",
    )
    shop_id: Mapped[UUID7 | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("shops.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
        comment="Foreign key to shops table",
    )
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        comment="Operator name",
    )

    # Relations
    retailer: Mapped["RetailersOrm"] = relationship(
        "RetailersOrm",
        back_populates="operators",
        lazy="selectin",
    )
    shop: Mapped["ShopsOrm"] = relationship(
        "ShopsOrm",
        back_populates="operators",
        lazy="selectin",
    )
    receipts: Mapped[list["ReceiptsOrm"]] = relationship(
        "ReceiptsOrm",
        back_populates="operator",
        lazy="selectin",
    )
