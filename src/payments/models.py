from sqlalchemy import SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.db import Base


class PaymentsOrm(Base):
    """Directory table of all payment types"""

    # See https://www.consultant.ru/document/cons_doc_LAW_362322/f5f1ab57b729060b906f8beaa1ea6d119c9607a4/ for ids
    id: Mapped[int] = mapped_column(
        SmallInteger,
        primary_key=True,
        index=True,
        unique=True,
        comment="Unique identifier of the payment type",
    )
    description: Mapped[str] = mapped_column(
        String,
        nullable=False,
        comment="Payment type description",
    )
    pf_format: Mapped[str] = mapped_column(
        String,
        nullable=False,
        comment="Short string code for print format of payment type",
    )
