from datetime import datetime, timezone
from decimal import Decimal
from re import IGNORECASE, sub

from fastapi import HTTPException, status
from pydantic import UUID7
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.transactional import transactional
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


class RegistryService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.crpt_service = CrptService(db)
        self.receipts_service = ReceiptsService(db)
        self.items_service = ItemsService(db)
        self.retailers_service = RetailersService(db)
        self.shops_service = ShopsService(db)
        self.employees_service = EmployeesService(db)

    def _str_clean(self, string: str | None) -> str | None:
        """Strips input and removes space duplication"""
        if string is None:
            return None

        string = sub(r"\s+", " ", string)
        string = string.strip()

        return string

    def _name_compress(self, name: str | None, inn: str) -> str | None:
        """Cleans and compresses abbrs of retailer name string"""
        if name is None:
            return None

        name = self._str_clean(name)
        name = sub(
            "ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ",
            "ООО",
            name,
            flags=IGNORECASE,
        )
        name = sub(
            "ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ КУЛЬТУРЫ",
            "ФГБУК",
            name,
            flags=IGNORECASE,
        )
        name = sub(
            "АКЦИОНЕРНОЕ ОБЩЕСТВО",
            "АО",
            name,
            flags=IGNORECASE,
        )
        name = sub(
            "ПУБЛИЧНОЕ АО",
            "ПАО",
            name,
            flags=IGNORECASE,
        )
        name = sub(
            "ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ КУЛЬТУРЫ",
            "ГБУК",
            name,
            flags=IGNORECASE,
        )
        name = sub(
            "ГОСУДАРСТВЕННОЕ УНИТАРНОЕ ПРЕДПРИЯТИЕ",
            "ГУП",
            name,
            flags=IGNORECASE,
        )

        if len(inn.strip()) == 12 and len(name) > 1 and name[:2].upper() != "ИП":
            name = f"ИП {name}"

        return name

    async def get(self, fiscal_fields: FiscalFields) -> Registry:
        receipt = await self.receipts_service.receipts_dao.get_by_fiscal_fields(
            fiscal_fields.t_datetime,
            fiscal_fields.s,
            fiscal_fields.fn,
            fiscal_fields.i,
            fiscal_fields.fp,
            fiscal_fields.n,
        )
        if not receipt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registry is not found by fiscal fields",
            )

        crpt = receipt.crpt
        items = receipt.items
        retailer = receipt.shop.retailer
        shop = receipt.shop
        employee = receipt.employee

        return Registry(
            crpt=Crpt.model_validate(crpt),
            receipt=Receipt.model_validate(receipt),
            items=[Item.model_validate(item) for item in items],
            retailer=Retailer.model_validate(retailer),
            shop=Shop.model_validate(shop) if shop else None,
            employee=Employee.model_validate(employee) if employee else None,
        )

    async def get_by_receipt_id(self, receipt_id: UUID7) -> Registry:
        receipt = await self.receipts_service.receipts_dao.get_by_id(receipt_id)
        if not receipt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Registry is not found by receipt with id {receipt_id}",
            )

        crpt = receipt.crpt
        items = receipt.items
        retailer = receipt.retailer
        shop = receipt.shop
        employee = receipt.employee

        return Registry(
            crpt=Crpt.model_validate(crpt),
            receipt=Receipt.model_validate(receipt),
            items=[Item.model_validate(item) for item in items],
            retailer=Retailer.model_validate(retailer),
            shop=Shop.model_validate(shop) if shop else None,
            employee=Employee.model_validate(employee) if employee else None,
        )

    @transactional
    async def create(self, fiscal_fields: FiscalFields) -> Registry:
        receipt = await self.receipts_service.receipts_dao.get_by_fiscal_fields(
            fiscal_fields.t_datetime,
            fiscal_fields.s,
            fiscal_fields.fn,
            fiscal_fields.i,
            fiscal_fields.fp,
            fiscal_fields.n,
        )
        if receipt:
            crpt = receipt.crpt
            items = receipt.items
            retailer = receipt.retailer
            shop = receipt.shop
            employee = receipt.employee

            return Registry(
                crpt=Crpt.model_validate(crpt),
                receipt=Receipt.model_validate(receipt),
                items=[Item.model_validate(item) for item in items],
                retailer=Retailer.model_validate(retailer),
                shop=Shop.model_validate(shop) if shop else None,
                employee=Employee.model_validate(employee) if employee else None,
            )

        dump = await self.crpt_service.get_from_crpt_api(fiscal_fields)
        crpt = await self.crpt_service.create(dump)

        inn = dump["fiscalData"]["receipt"]["userInn"]
        name = dump["fiscalData"]["receipt"].get("user", "")
        retailer = await self.retailers_service.create(
            inn=self._str_clean(inn),
            name=self._name_compress(name, inn),
        )

        address = dump["fiscalData"]["receipt"].get("retailPlaceAddress", None)
        shop = None
        if address:
            shop = await self.shops_service.create(
                retailer_id=retailer.id,
                address=self._str_clean(address),
            )

        name = dump["fiscalData"]["receipt"].get("operator", None)
        employee = None
        if name:
            employee = await self.employees_service.create(
                retailer_id=retailer.id,
                shop_id=shop.id if shop else None,
                name=self._str_clean(name),
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
            retailer_id=retailer.id,
            shop_id=shop.id if shop else None,
            employee_id=employee.id if employee else None,
            fiscal_fields=fiscal_fields,
        )

        items_data = dump["fiscalData"]["receipt"]["items"]
        items = []
        for item in items_data:
            name = item.get("name", None)
            price = Decimal(item["price"]) / 100
            quantity = item["quantity"]
            measure = item.get("itemsQuantityMeasure", 255)
            total = Decimal(item["sum"]) / 100
            nds = item.get("nds", 6)
            payment = item["paymentType"]
            product = item.get("productType", 4)
            items.append(
                {
                    "name": self._str_clean(name),
                    "price": price,
                    "quantity": quantity,
                    "measure": measure,
                    "total": total,
                    "nds": nds,
                    "payment": payment,
                    "product": product,
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
        crpt = await self.crpt_service.crpt_dao.get_by_qr_code(fiscal_fields.qr_code)
        if not crpt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registry not found by fiscal fields",
            )

        if crpt.is_orphan:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Can not delete registry, because it is orphan",
            )

        receipt = crpt.receipt
        items = receipt.items
        retailer = receipt.retailer
        shop = receipt.shop
        employee = receipt.employee

        # Skips orphan retailers, shops and employees on deletion
        crpt = await self.crpt_service.crpt_dao.delete(crpt)

        return Registry(
            crpt=Crpt.model_validate(crpt),
            receipt=Receipt.model_validate(receipt),
            items=[Item.model_validate(item) for item in items],
            retailer=Retailer.model_validate(retailer),
            shop=Shop.model_validate(shop) if shop else None,
            employee=Employee.model_validate(employee) if employee else None,
        )
