from fastapi import status, Request, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Query

from src.db.session import db_session
from src.models.invoices import Product, Invoice, Element
from src.models.users import User
from src.routers.v1.auth import manager
from src.routers.v1.settings import url_version
from src.schemas.invoices import ProductSchema, InvoiceCreate
from src.settings import TEMPLATES

router = APIRouter()

@router.get(f'{url_version}/products', status_code=status.HTTP_200_OK, tags=['Html'])
async def get_all_catalog(request: Request):
    with db_session() as session:
        return TEMPLATES.TemplateResponse('products_list.html', {'request': request, 'products': [ProductSchema(**product.__dict__).__dict__ for product in Query([Product], session=session).all()]})  # type: ignore


@router.post(f'{url_version}/invoices', tags=['Invoices'], status_code=status.HTTP_201_CREATED, response_model=InvoiceCreate)
def create_invoice(*, invoice_data: InvoiceCreate, user=Depends(manager)) -> InvoiceCreate:
    with db_session() as session:
        user = Query([User], session=session).filter(User.email == user['email']).first()
        invoice = Invoice(user=user)
        elements: list = []
        for element in invoice_data.elements:
            product = Query([Product], session=session).filter(Product.name == element.product_name).first()
            if product is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f'Product {element.product_name} not found')
            elements.append(Element(amount=element.amount,
                                    price=element.price,
                                    product=product,
                                    invoice=invoice))
        session.add(invoice)
        session.commit()
        session.bulk_save_objects(elements)
        return invoice_data


@router.get(f'{url_version}/invoices/all', tags=['Invoices'])
def get_user_invoices(user=Depends(manager)):
    with db_session() as session:
        if user['is_superuser'] is True:
            filtrado = True
        else:
            filtrado = User.email == user['email']

        return {'results': {user.email: [{'id': invoice.id,
                                          'total': invoice.total,
                                          'taxes': invoice.tax,
                                          'total_incl_taxes': invoice.total_inc_tax,
                                          'products': [{'name': element.product.name,
                                                        'price': element.price,
                                                        'amount': element.amount}
                                                       for element in invoice.elements]}
                                         for invoice in Query(Invoice, session=session).filter(Invoice.user == user).all()]
                            for user in Query(User, session=session).filter(filtrado).all()}}
