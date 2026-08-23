from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.products.dao import ProductsDao
from src.products.schemes import Product, ProductList


class ProductsService:
    def __init__(self, db: AsyncSession):
        self.products_dao = ProductsDao(db)

    async def get_all(self) -> ProductList:
        result = await self.products_dao.get_all()

        return ProductList(items=[Product.model_validate(item) for item in result])

    async def get_by_id(self, product_id: int) -> Product:
        result = await self.products_dao.get_by_id(product_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product type with id {product_id} not found ",
            )

        return Product.model_validate(result)
