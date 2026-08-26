from typing import TYPE_CHECKING, Any
from uuid import uuid7

from pydantic import UUID7
from sqlalchemy import Index, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base

if TYPE_CHECKING:
    from src.receipts.model import ReceiptsOrm


class CrptOrm(Base):
    """Table of all CRPT dumps from external API"""

    __table_args__ = (
        Index(
            "ix_crpt_dump_code",
            text("(dump->>'code')"),
        ),
    )

    id: Mapped[UUID7] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        unique=True,
        default=lambda: uuid7(),
        comment="Unique identifier for the receipt",
    )
    dump: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        comment="Full receipt dump in JSON format from CRPT API",
    )

    # Relations
    receipt: Mapped["ReceiptsOrm"] = relationship(
        "ReceiptsOrm",
        back_populates="crpt",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="selectin",
    )
