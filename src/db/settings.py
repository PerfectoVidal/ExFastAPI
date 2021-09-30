from dotenv import load_dotenv
import os

from src.users.models import User
from src.invoices.models import Invoice, Product, Catalog

load_dotenv()

uri_db = os.getenv('SQLALCHEMY_DATABASE_URI')

models_to_import = [User,
                    Invoice, Product, Catalog
                    ]


