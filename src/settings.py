from dotenv import load_dotenv
import os

from .users.models import User

load_dotenv()

uri_db = os.getenv('SQLALCHEMY_DATABASE_URI')

models_to_import = [User,
                    ]