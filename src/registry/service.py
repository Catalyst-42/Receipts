from datetime import datetime, timezone
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.crpt.dao import CrptDao
from src.crpt.schemes import Crpt
from src.crpt.service import CrptService
from src.employees.dao import EmployeesDao
from src.employees.schemes import Employee
from src.items.dao import ItemsDao
from src.items.schemes import Item, ItemList
from src.receipts.dao import ReceiptsDao
from src.receipts.schemes import FiscalFields, Receipt
from src.registry.schemes import Registry
from src.retailers.dao import RetailersDao
from src.retailers.schemes import Retailer
from src.shops.dao import ShopsDao
from src.shops.schemes import Shop


class RegistryService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.crpt_dao = CrptDao(db)
        self.receipts_dao = ReceiptsDao(db)
        self.items_dao = ItemsDao(db)
        self.retailers_dao = RetailersDao(db)
        self.shops_dao = ShopsDao(db)
        self.employees_dao = EmployeesDao(db)
        self.crpt_service = CrptService(db)

    async def create(self, fiscal_fields: FiscalFields) -> Registry:
        crpt = await self.crpt_dao.get_by_qr_code(fiscal_fields.qr_code)
        if crpt:
            receipt = crpt.receipt
            items = receipt.items
            retailer = receipt.shop.retailer
            shop = receipt.shop
            employee = receipt.employee

            return Registry(
                crpt=Crpt.model_validate(crpt),
                receipt=Receipt.model_validate(receipt),
                items=[Item.model_validate(item) for item in items],
                retailer=Retailer.model_validate(retailer),
                shop=Shop.model_validate(shop),
                employee=Employee.model_validate(employee),
            )

        dump = await self.crpt_service.get_from_crpt_api(fiscal_fields)
        crpt = await self.crpt_dao.create(dump)

        retailer = await self.retailers_dao.create(
            inn=dump["fiscalData"]["receipt"]["userInn"],
            name=dump["fiscalData"]["receipt"]["user"],
        )

        shop = await self.shops_dao.create(
            retailer_id=retailer.id,
            address=dump["fiscalData"]["receipt"]["retailPlaceAddress"],
        )

        employee = await self.employees_dao.create(
            shop_id=shop.id,
            name=dump["fiscalData"]["receipt"]["operator"],
        )

        code_data = dump["fiscalData"]["codeData"]
        t = datetime.fromtimestamp(
            code_data["fiscalDate"] / 1000,
            tz=timezone.utc,
        ).replace(tzinfo=None)
        s = Decimal(code_data["cost"]) / 100
        fn = code_data["fiscalDriveNumber"]
        i = code_data["fiscalDocumentNumber"]
        fp = code_data["fiscalSign"]
        n = code_data["operationType"]

        receipt = await self.receipts_dao.create(
            crpt_id=crpt.id,
            shop_id=shop.id,
            employee_id=employee.id,
            t=t,
            s=s,
            fn=fn,
            i=i,
            fp=fp,
            n=n,
        )

        items_data = dump["fiscalData"]["receipt"]["items"]
        items = []
        for item in items_data:
            items.append(
                {
                    "name": item["name"],
                    "price": item["price"],
                    "quantity": item["quantity"],
                    "measure": item["itemsQuantityMeasure"],
                    "total": item["sum"],
                    "nds": item["nds"],
                    "payment": item["paymentType"],
                    "product": item["productType"],
                }
            )
        items = await self.items_dao.create_many(receipt.id, items)

        return Registry(
            crpt=Crpt.model_validate(crpt),
            receipt=Receipt.model_validate(receipt),
            items=[Item.model_validate(item) for item in items],
            retailer=Retailer.model_validate(retailer),
            shop=Shop.model_validate(shop),
            employee=Employee.model_validate(employee),
        )

    async def delete(self, fiscal_fields: FiscalFields) -> Registry:
        crpt = await self.crpt_dao.get_by_qr_code(fiscal_fields.qr_code)
        if not crpt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Crpt record is not found",
            )

        crpt = await self.crpt_dao.delete(crpt)

        return Registry(
            crpt=Crpt.model_validate(crpt),
            receipt=Receipt.model_validate(crpt.receipt),
            items=[Item.model_validate(item) for item in crpt.receipt.items],
            retailer=Retailer.model_validate(crpt.receipt.shop.retailer),
            shop=Shop.model_validate(crpt.receipt.shop),
            employee=Employee.model_validate(crpt.receipt.employee)
        )
