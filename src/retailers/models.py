from typing import TYPE_CHECKING
from uuid import UUID, uuid7

from sqlalchemy import Computed, String
from sqlalchemy.dialects.postgresql import UUID as SQL_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base

if TYPE_CHECKING:
    from src.shops.models import ShopsOrm


class ShopsOrm(Base):
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
        comment="TIN (ИНН) of a company or a single persona",
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
    shops: Mapped[list["ShopsOrm"]] = relationship(
        "ShopsOrm",
        back_populates="retailer",
        lazy="selectin",
    )
