import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates

load_dotenv()

BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))
ACCESS_TOKEN_EXPIRE_MINUTES = 60
SECRET_KEY: str = os.getenv('SECRET_KEY') if os.getenv('SECRET_KEY') else '' # type: ignore
ALGORITHM = os.getenv('ALGORITHM_JWT')

TAXES = float(os.getenv('TAXES'))  # type: ignore
