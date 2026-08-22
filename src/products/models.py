from sqlalchemy import SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.db import Base


class ProductsOrm(Base):
    """Directory table of all product types"""

    # See https://www.consultant.ru/document/cons_doc_LAW_362322/0060b1f1924347c03afbc57a8d4af63888f81c6c/ for ids
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
