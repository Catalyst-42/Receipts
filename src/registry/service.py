from datetime import datetime, timezone
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.crpt.schemes import Crpt
from src.crpt.service import CrptService
from src.employees.schemes import Employee
from src.employees.service import EmployeesService
from src.items.schemes import Item
from src.items.service import ItemsService
from src.receipts.schemes import FiscalFields, Receipt
from src.receipts.service import ReceiptsService
from src.registry.schemes import Registry
from src.retailers.schemes import Retailer
from src.retailers.service import RetailersService
from src.shops.schemes import Shop
from src.shops.service import ShopsService
from src.core.transactional import transactional


class RegistryService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.crpt_service = CrptService(db)
        self.receipts_service = ReceiptsService(db)
        self.items_service = ItemsService(db)
        self.retailers_service = RetailersService(db)
        self.shops_service = ShopsService(db)
        self.employees_service = EmployeesService(db)

    @transactional
    async def create(self, fiscal_fields: FiscalFields) -> Registry:
        crpt = await self.crpt_service.crpt_dao.get_by_qr_code(fiscal_fields.qr_code)
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
                employee=Employee.model_validate(employee) if employee else None,
            )

        dump = await self.crpt_service.get_from_crpt_api(fiscal_fields)
        crpt = await self.crpt_service.create(dump)

        inn = dump["fiscalData"]["receipt"]["userInn"].strip()
        name = dump["fiscalData"]["receipt"]["user"].strip()
        retailer = await self.retailers_service.create(
            inn=inn,
            name=name,
        )

        address = dump["fiscalData"]["receipt"].get("retailPlaceAddress", None)
        shop = await self.shops_service.create(
            retailer_id=retailer.id,
            address=address,
        )

        name = dump["fiscalData"]["receipt"].get("operator", None)
        employee = None
        if name:
            employee = await self.employees_service.create(
                shop_id=shop.id,
                name=name,
            )

        code_data = dump["fiscalData"]["codeData"]
        t = (
            datetime.fromtimestamp(
                code_data["fiscalDate"] / 1000,
                tz=timezone.utc,
            )
            .replace(tzinfo=None)
            .strftime("%Y%m%dT%H%M")
        )
        s = Decimal(dump["fiscalData"]["codeData"]["cost"]) / 100
        fn = dump["fiscalData"]["codeData"]["fiscalDriveNumber"]
        i = dump["fiscalData"]["codeData"]["fiscalDocumentNumber"]
        fp = dump["fiscalData"]["codeData"]["fiscalSign"]
        n = dump["fiscalData"]["codeData"]["operationType"]

        fiscal_fields = FiscalFields(t=t, s=s, fn=fn, i=i, fp=fp, n=n)
        receipt = await self.receipts_service.create(
            crpt_id=crpt.id,
            shop_id=shop.id,
            employee_id=employee.id if employee else None,
            fiscal_fields=fiscal_fields,
        )

        items_data = dump["fiscalData"]["receipt"]["items"]
        items = []
        for item in items_data:
            items.append(
                {
                    "name": item["name"],
                    "price": Decimal(item["price"]) / 100,
                    "quantity": item["quantity"],
                    "measure": item.get("itemsQuantityMeasure", 255),
                    "total": Decimal(item["sum"]) / 100,
                    "nds": item["nds"],
                    "payment": item["paymentType"],
                    "product": item["productType"],
                }
            )
        items = await self.items_service.create_many(receipt.id, items)

        return Registry(
            crpt=crpt,
            receipt=receipt,
            items=items.items,
            retailer=retailer,
            shop=shop,
            employee=employee,
        )

    @transactional
    async def delete(self, fiscal_fields: FiscalFields) -> Registry:
        crpt = await self.crpt_service.get_by_qr_code(fiscal_fields.qr_code)
        if not crpt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registry not found by fiscal fields",
            )

        # Skip orphans
        crpt = await self.crpt_service.delete(crpt)

        return Registry(
            crpt=Crpt.model_validate(crpt),
            receipt=Receipt.model_validate(crpt.receipt),
            items=[Item.model_validate(item) for item in crpt.receipt.items],
            retailer=Retailer.model_validate(crpt.receipt.shop.retailer),
            shop=Shop.model_validate(crpt.receipt.shop),
            employee=Employee.model_validate(crpt.receipt.employee),
        )
