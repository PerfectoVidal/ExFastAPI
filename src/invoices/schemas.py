from decimal import Decimal

from pydantic import BaseModel


class ProductSchema(BaseModel):
    name: str
    price: Decimal
