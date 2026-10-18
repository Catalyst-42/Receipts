from pydantic import BaseModel

from src.users.schemas import Owner
from src.crpt.schemas import Crpt
from src.operators.schemas import Operator
from src.items.schemas import Item
from src.receipts.schemas import Receipt
from src.retailers.schemas import Retailer
from src.shops.schemas import Shop


class Registry(BaseModel):
    owner: Owner
    crpt: Crpt
    receipt: Receipt
    items: list[Item]
    retailer: Retailer
    shop: Shop | None
    operator: Operator | None
