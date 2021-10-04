from fastapi import APIRouter, status, HTTPException
from sqlalchemy.orm import Query

from src.db.session import session
from src.users.models import User
from src.users.schemas import UserList, UserResult, UserCreate

router = APIRouter()


@router.get("/api/v1/users/", tags=["users"], status_code=status.HTTP_200_OK, response_model=UserList)
async def read_all_users():
    q = Query([User], session=session).all()
    if q:
        return {'results': [UserResult(**user.__dict__) for user in q]}


@router.post("/api/v1/users/", tags=["users"], status_code=status.HTTP_201_CREATED, response_model=UserCreate)
async def create_user(*, user_data: UserCreate) -> dict:
    data = user_data.__dict__
    data['is_superuser'] = False
    session.add(User(**data))
    session.commit()
    return data


@router.get("/api/v1/users/{name}", tags=["users"], status_code=status.HTTP_200_OK, response_model=UserResult)
async def search_user(name: str):
    q = Query([User], session=session).filter(User.name == name).first()
    if q:
        return UserResult(**q.__dict__)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"The user with name {name} not found")
