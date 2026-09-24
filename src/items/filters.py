from decimal import Decimal
from uuid import UUID

from fastapi_filter.contrib.sqlalchemy import Filter

from src.items.model import ItemsOrm


class ItemsFilters(Filter):
    name__ilike: str | None = None
    name__eq: str | None = None
    price__gte: Decimal | None = None
    price__lte: Decimal | None = None
    total__gte: Decimal | None = None
    total__lte: Decimal | None = None
    quantity__gte: float | None = None
    quantity__lte: float | None = None

    measure__in: list[int] | None = None
    nds__in: list[int] | None = None
    payment__in: list[int] | None = None
    product__in: list[int] | None = None

    order_by: list[str] | None = None

    class Constants(Filter.Constants):
        model = ItemsOrm
        ordering_field_name = "order_by"
