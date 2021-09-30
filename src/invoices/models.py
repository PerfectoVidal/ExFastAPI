from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship

from src.db.base import Base


class Invoice(Base):
    __tablename__ = 'invoices'
    id = Column(Integer, primary_key=True, index=True)
    products = relationship("Product",
                            cascade="all,delete-orphan",
                            back_populates="products",
                            uselist=True,
                            )


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
                            back_populates="products",
                            uselist=True,
                            )
