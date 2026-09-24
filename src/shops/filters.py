from decimal import Decimal
from uuid import UUID

from fastapi_filter.contrib.sqlalchemy import Filter

from src.shops.model import ShopsOrm


class ShopsFilters(Filter):
    address__ilike: str | None = None

    order_by: list[str] | None = None

    class Constants(Filter.Constants):
        model = ShopsOrm
        ordering_field_name = "order_by"
