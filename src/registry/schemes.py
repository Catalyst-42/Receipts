from pydantic import BaseModel

from src.users.schemes import Owner
from src.crpt.schemes import Crpt
from src.employees.schemes import Employee
from src.items.schemes import Item
from src.receipts.schemes import Receipt
from src.retailers.schemes import Retailer
from src.shops.schemes import Shop


class Registry(BaseModel):
    owner: Owner
    crpt: Crpt
    receipt: Receipt
    items: list[Item]
    retailer: Retailer
    shop: Shop | None
    employee: Employee | None
