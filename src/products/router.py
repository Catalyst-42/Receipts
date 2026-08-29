from typing import Annotated

from fastapi import Depends, Path
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.core.schemes import ErrorResponse
from src.products.schemes import GetProductByIdRequest, Product, ProductList
from src.products.service import ProductsService
from src.core.schemes import Count

router = APIRouter(prefix="/products", tags=["Products"])


def get_products_service(db: AsyncSession = Depends(get_db)):
    return ProductsService(db)


@router.get("/", response_model=ProductList)
async def get_product_types(
    products_service: ProductsService = Depends(get_products_service),
) -> ProductList:
    """Returns all directory of product types"""
    result = await products_service.get_all()
    return result


@router.get(
    "/stats/count",
    response_model=Count,
)
async def get_receipts_count(
    products_service: ProductsService = Depends(get_products_service),
) -> Count:
    """Returns total count of product types in database"""
    return await products_service.get_count()


@router.get(
    "/{product_id}",
    response_model=Product,
    responses={
        404: {"model": ErrorResponse, "description": "product type not found"},
    },
)
async def get_product_type(
    request: Annotated[GetProductByIdRequest, Path()],
    products_service: ProductsService = Depends(get_products_service),
) -> Product:
    """Finds product type by its id"""
    result = await products_service.get_by_id(request.product_id)
    return result
