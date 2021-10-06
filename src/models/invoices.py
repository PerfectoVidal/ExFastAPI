from functools import lru_cache

from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship

from src.db.base import Base
from src.settings import TAXES


class Invoice(Base):
    __tablename__ = 'invoices'
    id = Column(Integer, primary_key=True, index=True)
    elements = relationship("Element", cascade="all", back_populates="invoice")  # type: ignore
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="invoices", cascade="all")  # type: ignore

    @property  # type: ignore
    @lru_cache(maxsize=64)  # type: ignore
    def total(self) -> float:
        return sum([float(element.price) * element.amount for element in self.elements])

    @property  # type: ignore
    @lru_cache(maxsize=64)  # type: ignore
    def tax(self) -> float:
        return self.total * TAXES  # type: ignore

    @property  # type: ignore
    @lru_cache(maxsize=64)  # type: ignore
    def total_inc_tax(self) -> float:
        return self.tax + self.total  # type: ignore


class Element(Base):
    __tablename__ = 'elements'
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, nullable=False)
    price = Column(DECIMAL(10, 2))
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    product = relationship("Product", back_populates="invoice_element")  # type: ignore
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=True)
    invoice = relationship("Invoice", back_populates="elements", cascade="all")  # type: ignore


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), unique=True)
    price = Column(DECIMAL(10, 2))
    invoice_element = relationship("Element", back_populates="product", uselist=True)  # type: ignore
