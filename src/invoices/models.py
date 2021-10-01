from functools import lru_cache

from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship

from src.db.base import Base
from src.settings import taxes


class Invoice(Base):
    __tablename__ = 'invoices'
    id = Column(Integer, primary_key=True, index=True)
    elements = relationship("Element", cascade="all", back_populates="invoice")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="invoices", cascade="all")

    @property
    @lru_cache(maxsize=64)
    def total(self) -> float:
        return sum([float(element.price) * element.amount for element in self.elements])

    @property
    @lru_cache(maxsize=64)
    def tax(self) -> float:
        return self.total * taxes

    @property
    @lru_cache(maxsize=64)
    def total_inc_tax(self) -> float:
        return self.tax + self.total


class Element(Base):
    __tablename__ = 'elements'
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, nullable=False)
    price = Column(DECIMAL(10, 2))
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    product = relationship("Product", back_populates="invoice_element")
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=True)
    invoice = relationship("Invoice", back_populates="elements", cascade="all", )


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))
    price = Column(DECIMAL(10, 2))
    invoice_element = relationship("Element",
                                   back_populates="product",
                                   uselist=True,
                                   )
