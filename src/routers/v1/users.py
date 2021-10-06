from fastapi import status, HTTPException, APIRouter
from sqlalchemy.orm import Query

from src.db.session import db_session
from src.models.users import User
from src.routers.v1.settings import url_version
from src.schemas.users import UserResult, UserCreate, UserList

router = APIRouter()


@router.get(f'{url_version}/users/', tags=['Users'], status_code=status.HTTP_200_OK, response_model=UserList)
async def read_all_users():
    with db_session() as session:
        q = Query([User], session=session).all()
        if q:
            return {'results': [UserResult(**user.__dict__) for user in q]}


@router.post(f'{url_version}/users/', tags=['Users'], status_code=status.HTTP_201_CREATED, response_model=UserCreate)
async def create_user(*, user_data: UserCreate) -> dict:
    with db_session() as session:
        data = user_data.__dict__
        data['is_superuser'] = False
        session.add(User(**data))
        session.commit()
        return data


@router.get('{}/users/{}'.format(url_version, '{name}'), tags=['Users'], status_code=status.HTTP_200_OK, response_model=UserResult)
async def search_user(name: str):
    with db_session() as session:
        q = Query([User], session=session).filter(User.name == name).first()
        if q:
            return UserResult(**q.__dict__)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The user with name {name} not found')
