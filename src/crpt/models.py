from uuid import uuid7

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB, UUID

from src.core.db import Base


class CrptOrm(Base):
    """Table of all CRPT dumps from external API"""

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=lambda: uuid7(),
        unique=True,
        comment="Unique identifier for the receipt",
    )
    dump = Column(
        JSONB,
        nullable=False,
        comment="Full receipt data in JSON format from CRPT API",
    )
