from typing import TYPE_CHECKING
from uuid import uuid7

from pydantic import UUID7
from sqlalchemy import ForeignKey, Index, String, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base

if TYPE_CHECKING:
    from src.employees.model import EmployeesOrm
    from src.receipts.model import ReceiptsOrm
    from src.retailers.model import RetailersOrm


class ShopsOrm(Base):
    """Table of all shops by retailers"""

    __table_args__ = (
        UniqueConstraint("retailer_id", "address"),
        Index(
            "ix_unique_online_shop_per_retailer",
            "retailer_id",
            unique=True,
            postgresql_where=text("address IS NULL"),
        ),
    )

    id: Mapped[UUID7] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        unique=True,
        default=lambda: uuid7(),
        comment="Unique identifier for the retailer",
    )
    retailer_id: Mapped[UUID7] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("retailers_orm.id", ondelete="CASCADE"),
        index=True,
        unique=True,
        comment="Link on retailer - owner of this shop",
    )
    address: Mapped[str | None] = mapped_column(
        String(),
        nullable=True,
        comment="Physical address of a shop. Null if shop is online one",
    )

    # Relations
    receipts: Mapped[list["ReceiptsOrm"]] = relationship(
        "ReceiptsOrm",
        back_populates="shop",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    retailer: Mapped["RetailersOrm"] = relationship(
        "RetailersOrm",
        back_populates="shops",
        lazy="selectin",
    )
    employees: Mapped[list["EmployeesOrm"]] = relationship(
        "EmployeesOrm",
        back_populates="shop",
        lazy="selectin",
    )
