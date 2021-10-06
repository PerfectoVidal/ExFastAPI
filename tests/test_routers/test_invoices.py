from decimal import Decimal
from unittest.mock import patch

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy.orm import Query

from main import app
from src.models.invoices import Product, Invoice, Element
from src.models.users import User
from src.routers.v1.invoices import create_invoice, get_user_invoices
from src.schemas.invoices import InvoiceCreate, ElementSchema

client = TestClient(app)


class TestRouters:
    def test_get_all_catalog(self, dbsession):
        with patch('src.routers.v1.invoices.db_session', return_value=dbsession):
            with patch('src.routers.v1.invoices.TEMPLATES') as TEMPLATES:
                client.get("/api/v1/products")
                assert TEMPLATES.TemplateResponse.called

    def test_create_invoice_product_not_found(self, dbsession):
        with pytest.raises(HTTPException) as excinfo:
            with patch('src.routers.v1.invoices.db_session', return_value=dbsession):
                invoice_data = InvoiceCreate(elements=[ElementSchema(amount=1, price=Decimal(10), product_name='producto1')])
                user = {'email': ''}
                create_invoice(invoice_data=invoice_data, user=user)
        assert all([excinfo.value.status_code == 404,
                    excinfo.value.detail == 'Product producto1 not found'])

    def test_create_invoice(self, dbsession):
        with patch('src.routers.v1.invoices.db_session', return_value=dbsession):
            facturas_iniciales = Query([Invoice], session=dbsession).count()
            elementos_iniciales = Query([Element], session=dbsession).count()
            dbsession.add(User(name='foo', surname_1='surfoo1', surname_2='surfoo2', password='1234', email='foo@gmail.com', is_superuser=False))
            dbsession.add(Product(name='producto1', price=10))
            dbsession.commit()

            invoice_data = InvoiceCreate(elements=[ElementSchema(amount=1, price=Decimal(10), product_name='producto1')])

            user = {'email': 'foo@gmail.com'}
            create_invoice(invoice_data=invoice_data, user=user)
        assert all([facturas_iniciales == 0,
                    elementos_iniciales == 0,
                    Query([Invoice], session=dbsession).count() == 1,
                    Query([Element], session=dbsession).count() == 1])

    def test_get_user_invoices_normal_user(self, dbsession):
        with patch('src.routers.v1.invoices.db_session', return_value=dbsession):
            user_normal = User(name='foo', surname_1='surfoo1', surname_2='surfoo2', password='1234', email='foo@gmail.com', is_superuser=False)
            super_user = User(name='fooSuper', surname_1='surfoo1', surname_2='surfoo2', password='1234', email='fooSuper@gmail.com', is_superuser=True)
            dbsession.add(user_normal)
            dbsession.add(super_user)
            dbsession.commit()
            producto = Product(name='producto1', price=10)
            dbsession.add(producto)
            dbsession.commit()
            invoice_normal = Invoice(user=user_normal)
            invoice_super = Invoice(user=super_user)
            dbsession.add(invoice_normal)
            dbsession.add(invoice_super)
            dbsession.commit()

            dbsession.add(Element(amount=1, price=10, product=producto,
                                  invoice=invoice_normal))
            dbsession.add(Element(amount=2, price=8, product=producto,
                                  invoice=invoice_super))
            dbsession.commit()

            assert get_user_invoices({'is_superuser': False, 'email': 'foo@gmail.com'}) == {'results': {'foo@gmail.com':
                                                                                                            [{'id': 1,
                                                                                                              'total': 10.0,
                                                                                                              'taxes': 2.1,
                                                                                                              'total_incl_taxes': 12.1,
                                                                                                              'products': [{'name': 'producto1',
                                                                                                                            'price': Decimal('10.00'),
                                                                                                                            'amount': 1}]}]}}

    def test_get_user_invoices_super_user(self, dbsession):
        with patch('src.routers.v1.invoices.db_session', return_value=dbsession):
            user_normal = User(name='foo', surname_1='surfoo1', surname_2='surfoo2', password='1234', email='foo@gmail.com', is_superuser=False)
            super_user = User(name='fooSuper', surname_1='surfoo1', surname_2='surfoo2', password='1234', email='fooSuper@gmail.com', is_superuser=True)
            dbsession.add(user_normal)
            dbsession.add(super_user)
            dbsession.commit()
            producto = Product(name='producto1', price=10)
            dbsession.add(producto)
            dbsession.commit()
            invoice_normal = Invoice(user=user_normal)
            invoice_super = Invoice(user=super_user)
            dbsession.add(invoice_normal)
            dbsession.add(invoice_super)
            dbsession.commit()

            dbsession.add(Element(amount=1, price=10, product=producto,
                                  invoice=invoice_normal))
            dbsession.add(Element(amount=2, price=8, product=producto,
                                  invoice=invoice_super))
            dbsession.commit()

            assert get_user_invoices({'is_superuser': True, 'email': 'fooSuper@gmail.com'}) == {'results': {'foo@gmail.com': [{'id': 1,
                                                                                                                               'total': 10.0,
                                                                                                                               'taxes': 2.1,
                                                                                                                               'total_incl_taxes': 12.1,
                                                                                                                               'products': [{'name': 'producto1',
                                                                                                                                             'price': Decimal('10.00'),
                                                                                                                                             'amount': 1}]}],
                                                                                                            'foosuper@gmail.com': [{'id': 2,
                                                                                                                                    'total': 16.0,
                                                                                                                                    'taxes': 3.36,
                                                                                                                                    'total_incl_taxes': 19.36,
                                                                                                                                    'products': [{'name': 'producto1',
                                                                                                                                                  'price': Decimal('8.00'),
                                                                                                                                                  'amount': 2}]}]}}
