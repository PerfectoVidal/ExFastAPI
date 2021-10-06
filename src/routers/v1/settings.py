from fastapi_login import LoginManager

from src.settings import SECRET_KEY

url_version = '/api/v1'
manager = LoginManager(SECRET_KEY, token_url=f'{url_version}/login')
