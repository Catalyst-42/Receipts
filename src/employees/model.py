from typing import TYPE_CHECKING
from uuid import uuid7

from pydantic import UUID7
from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base

if TYPE_CHECKING:
    from src.receipts.model import ReceiptsOrm
    from src.shops.model import RetailersOrm


class EmployeesOrm(Base):
    """Table of all employess by shops"""

    __table_args__ = (UniqueConstraint("shop_id", "name"),)

    id: Mapped[UUID7] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        unique=True,
        default=lambda: uuid7(),
        comment="Unique identifier for the employee",
    )
    shop_id: Mapped[UUID7] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("shops_orm.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Foreign key to shops table",
    )
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        comment="Employee name",
    )

    # Relations
    shop: Mapped["RetailersOrm"] = relationship(
        "ShopsOrm",
        back_populates="employees",
        lazy="selectin",
    )
    receipts: Mapped[list["ReceiptsOrm"]] = relationship(
        "ReceiptsOrm",
        back_populates="employee",
        lazy="selectin",
    )
