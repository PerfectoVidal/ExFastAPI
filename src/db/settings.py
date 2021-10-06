import os
from typing import List

from dotenv import load_dotenv

from src.models.invoices import Invoice, Product, Element
from src.models.users import User

load_dotenv()

uri_db: str = os.getenv('SQLALCHEMY_DATABASE_URI')  # type: ignore
create_tables: bool = True if os.getenv('CREATE_TABLES') == 'TRUE' else False

models_to_import: List = [User,
                          Invoice, Product, Element
                          ]
