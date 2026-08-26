from sqlalchemy import SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.db import Base


class ProductsOrm(Base):
    """Directory table of all product types"""

    # See https://www.consultant.ru/document/cons_doc_LAW_362322/cc1e361ee41688e67fe65c4740a242a10c265c86/ for ids
    id: Mapped[int] = mapped_column(
        SmallInteger,
        primary_key=True,
        index=True,
        unique=True,
        comment="Unique identifier of the VAT (НДС)",
    )
    description: Mapped[str] = mapped_column(
        String,
        nullable=False,
        comment="VAT (НДС) description",
    )
    pf_format: Mapped[str] = mapped_column(
        String,
        nullable=False,
        comment="Short string code for print format of payment type",
    )
