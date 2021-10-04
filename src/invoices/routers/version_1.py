from fastapi import APIRouter, status, Request
from sqlalchemy.orm import Query

from src.db.session import get_db
from src.invoices.models import Product
from src.invoices.schemas import ProductSchema
from src.settings import TEMPLATES

router = APIRouter()
session = get_db()


@router.get("/api/v1/products/", status_code=status.HTTP_200_OK, tags=["html"])
def get_all_catalog(request: Request) -> dict:
    return TEMPLATES.TemplateResponse(
        "products_list.html",
        {"request": request, "products": [ProductSchema(**product.__dict__).__dict__
                                          for product in Query(Product, session=session).all()]},
    )
