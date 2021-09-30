import os

from dotenv import load_dotenv

load_dotenv()

taxes = float(os.getenv('TAXES'))
