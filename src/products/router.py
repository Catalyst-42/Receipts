from typing import Annotated

from fastapi import Depends, Path
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.core.schemes import ErrorResponse
from src.products.schemes import GetProductByIdRequest, Product, ProductList
from src.products.service import ProductsService

router = APIRouter(prefix="/products", tags=["Products"])


def get_measures_service(db: AsyncSession = Depends(get_db)):
    return ProductsService(db)


@router.get("/", response_model=ProductList)
async def get_product_types(
    service: ProductsService = Depends(get_measures_service),
) -> ProductList:
    """Returns all directory of product types"""
    result = await service.get_all()
    return result


@router.get(
    "/{product_id}",
    response_model=Product,
    responses={
        404: {"model": ErrorResponse, "description": "product type not found"},
    },
)
async def get_product_type(
    request: Annotated[GetProductByIdRequest, Path()],
    service: ProductsService = Depends(get_measures_service),
) -> Product:
    """Finds product type by its id"""
    result = await service.get_by_id(request.product_id)
    return result
