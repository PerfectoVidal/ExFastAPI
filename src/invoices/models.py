from functools import lru_cache

from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship

from src.db.base import Base
from src.settings import taxes


class Invoice(Base):
    __tablename__ = 'invoices'
    id = Column(Integer, primary_key=True, index=True)
    products = relationship("Product", cascade="all", back_populates="invoice")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="invoices", cascade="all")

    @property
    @lru_cache(maxsize=64)
    def total(self) -> float:
        return sum([product.price * product.amout for product in self.products])

    @property
    @lru_cache(maxsize=64)
    def tax(self) -> float:
        return self.total * taxes

    @property
    @lru_cache(maxsize=64)
    def total_inc_tax(self) -> float:
        return self.tax + self.total


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, nullable=False)
    price = Column(DECIMAL(10, 2))
    catalogue_id = Column(Integer, ForeignKey("catalogue.id"), nullable=True)
    catalogue_item = relationship("Catalog", back_populates="products")
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=True)
    invoice = relationship("Invoice", back_populates="products", cascade="all", )


class Catalog(Base):
    __tablename__ = 'catalogue'
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(256))
    price = Column(DECIMAL(10, 2))
    products = relationship("Product",
                            back_populates="catalogue_item",
                            uselist=True,
                            )
