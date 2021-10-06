from decimal import Decimal
from typing import List

from pydantic import BaseModel


class ProductSchema(BaseModel):
    name: str
    price: Decimal


class ElementSchema(BaseModel):
    amount: int
    price: Decimal
    product_name: str


class InvoiceCreate(BaseModel):
    elements: List[ElementSchema]
