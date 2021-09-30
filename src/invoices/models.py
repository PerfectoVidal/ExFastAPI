from functools import lru_cache

from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship

from src.db.base import Base
from src.settings import taxes


class Invoice(Base):
    __tablename__ = 'invoices'
    id = Column(Integer, primary_key=True, index=True)
    products = relationship("Product",
                            cascade="all,delete-orphan",
                            backref="products",
                            uselist=True,
                            )
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    User = relationship("User", back_populates="users", cascade="all,delete-orphan", )

    @property
    @lru_cache(maxsize=64)
    def total(self) -> float:
        return sum([product.price * product.invoice for product in self.products])

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
    catalog_id = Column(Integer, ForeignKey("catalog.id"), nullable=True)
    catalog = relationship("Catalog", back_populates="catalog")
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=True)
    invoice = relationship("Invoice", back_populates="invoices", cascade="all,delete-orphan", )


class Catalog(Base):
    __tablename__ = 'catalog'
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(256))
    price = Column(DECIMAL(10, 2))
    products = relationship("Product",
                            backref="products",
                            uselist=True,
                            )
