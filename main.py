from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from user import schemas, models, crud
from settings_db import Session as SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/api/users", response_model=models.User)
def signup(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """add new user"""
    user = crud.get_user_by_email(db, user_data.email)
    if user:
        raise HTTPException(status_code=409,
                            detail="Email already registered.")
    signedup_user = crud.create_user(db, user_data)
    return signedup_user
