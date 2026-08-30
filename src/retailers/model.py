from typing import TYPE_CHECKING
from uuid import UUID, uuid7

from sqlalchemy import Computed, String
from sqlalchemy.dialects.postgresql import UUID as SQL_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base

if TYPE_CHECKING:
    from src.employees.model import EmployeesOrm
    from src.receipts.model import ReceiptsOrm
    from src.shops.model import ShopsOrm


class RetailersOrm(Base):
    """Table of all retailers (companies)"""

    id: Mapped[UUID] = mapped_column(
        SQL_UUID(as_uuid=True),
        primary_key=True,
        index=True,
        unique=True,
        default=lambda: uuid7(),
        comment="Unique identifier for the retailer",
    )
    inn: Mapped[str] = mapped_column(
        String(12),
        nullable=False,
        unique=True,
        comment="INN (TIN) of a company or a single persona",
    )
    is_individual: Mapped[bool] = mapped_column(
        Computed("length(inn) = 12", persisted=True),
        comment="Flag is the retailer is individual one, company otherwise",
    )
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        comment="Name of a company or a persona",
    )

    # Relations
    receipts: Mapped[list["ReceiptsOrm"]] = relationship(
        "ReceiptsOrm",
        back_populates="retailer",
        lazy="selectin",
    )
    shops: Mapped[list["ShopsOrm"]] = relationship(
        "ShopsOrm",
        back_populates="retailer",
        lazy="selectin",
    )
    employees: Mapped[list["EmployeesOrm"]] = relationship(
        "EmployeesOrm",
        back_populates="retailer",
        lazy="selectin",
    )
