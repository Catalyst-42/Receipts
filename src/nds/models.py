from sqlalchemy import SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.db import Base


class NdsOrm(Base):
    """Directory table of all VAT (НДС) types"""

    # See https://www.consultant.ru/document/cons_doc_LAW_362322/338afff6ce138d548f34d24c40f7a7b1c2185ecc/ for ids
    id: Mapped[int] = mapped_column(
        SmallInteger,
        primary_key=True,
        index=True,
        unique=True,
        comment="Unique identifier of the VAT (НДС)",
    )
    rate_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        comment="Short tax rate name",
    )
    pf_format: Mapped[str] = mapped_column(
        String,
        nullable=False,
        comment="Short string code for print format of VAT type",
    )
