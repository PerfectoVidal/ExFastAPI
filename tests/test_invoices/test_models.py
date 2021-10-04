from src.invoices.models import Invoice, Element, Product
from src.users.models import User
from sqlalchemy.orm import Query


class TestInvoice:
    def test_read_all_users(self, dbsession):
        user = User(name='foo', surname_1='surfoo1', surname_2='surfoo2', password='1234', email='foo@gmail.com', is_superuser=False)
        dbsession.add(user)
        dbsession.commit()

        invoice = Invoice(user=user)
        dbsession.add(invoice)
        dbsession.commit()

        product1 = Product(name='Producto1', price=20)
        product2 = Product(name='Producto2', price=30)
        dbsession.add(product1)
        dbsession.add(product2)
        dbsession.commit()

        dbsession.bulk_save_objects([Element(amount=2, price=product1.price, product=product1, invoice=invoice),
                                     Element(amount=2, price=product2.price, product=product2, invoice=invoice)])
        dbsession.commit()
        assert all([invoice.tax == 21,
                    invoice.total == 100,
                    invoice.total_inc_tax == 121])
