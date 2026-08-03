from uuid import uuid7

from sqlalchemy import JSON, Column, DateTime, String, func

from src.core.db import Base


class ReceiptsOrm(Base):
    """Table of all receipts gathered from exteral API"""

    __tablename__ = "receipts_orm"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid7()))
    qr_code = Column(String, unique=True, index=True, nullable=False)
    receipt_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
