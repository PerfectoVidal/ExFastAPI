from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from sqlalchemy.orm import Query

from src.db.session import db_session
from src.models.users import User
from src.routers.v1.settings import manager, url_version
from src.schemas.users import UserResult

router = APIRouter()


@router.post(f'{url_version}/login', tags=["Auth"])
def login(data: OAuth2PasswordRequestForm = Depends()):
    with db_session() as session:
        email = data.username
        password = data.password

        user = Query([User], session=session).filter(User.email == email).first()
        if not user:
            raise InvalidCredentialsException
        elif password != user.password:
            raise InvalidCredentialsException

        access_token = manager.create_access_token(
            data={'sub': email}
        )
        return {'access_token': access_token, 'token_type': 'bearer'}


@router.get(f'{url_version}/protected/me', tags=["Auth"])
def get_me(user=Depends(manager)):
    return {'user': UserResult(**user)}


@manager.user_loader()
def user_loader(email: str):
    with db_session() as session:
        user = Query([User], session=session).filter(User.email == email).first()
        return user.__dict__
