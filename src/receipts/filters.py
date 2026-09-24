from datetime import datetime

from fastapi_filter.contrib.sqlalchemy import Filter

from src.receipts.model import ReceiptsOrm


class ReceiptsFilters(Filter):
    s__gte: float | None = None
    s__lte: float | None = None
    t__gte: datetime | None = None
    t__lte: datetime | None = None

    order_by: list[str] | None = None

    class Constants(Filter.Constants):
        model = ReceiptsOrm
        ordering_field_name = "order_by"
