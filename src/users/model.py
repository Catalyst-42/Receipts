from typing import TYPE_CHECKING
from uuid import uuid7

from pydantic import UUID7
from sqlalchemy import Boolean, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base

if TYPE_CHECKING:
    from src.receipts.model import ReceiptsOrm


class UsersOrm(Base):
    id: Mapped[UUID7] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid7,
        index=True,
        unique=True,
        comment="Unique identifier of a user",
    )
    username: Mapped[str] = mapped_column(
        String(16),
        unique=True,
        nullable=False,
        index=True,
        comment="Unique user name",
    )
    hashed_password: Mapped[str] = mapped_column(
        String(60),
        nullable=False,
        comment="Hashed password from user account",
    )
    is_admin: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
        comment="Flag if user have additional privilegies",
    )

    # Relations
    receipts: Mapped[list["ReceiptsOrm"]] = relationship(
        "ReceiptsOrm",
        back_populates="owner",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
