from datetime import date, timedelta
from typing import List

from fastapi import Depends, HTTPException, status, Path, APIRouter, Query
from sqlalchemy import extract
from sqlalchemy.orm import Session

from src.schemas import UserResponse, UserModel
from src.database.db import get_db
from src.database.models import User
from src.repository import users as repository_users

router = APIRouter(prefix="/users", tags=['users'])


@router.get("/", response_model=List[UserResponse], name="All users:")
async def get_users(db: Session = Depends(get_db)):
    users = await repository_users.get_users(db)
    return users


@router.get("/birthday", response_model=List[UserResponse], name="Congratulate:")
async def get_users_by_birth_date(start_date: date = Query(default=date.today()),
                                  end_date: date = Query(default=(date.today() + timedelta(days=7))),
                                  db: Session = Depends(get_db)):
    users = db.query(User).filter(extract('day', User.birthday) >= start_date.day,
                                  extract('month', User.birthday) >= start_date.month,
                                  extract('day', User.birthday) <= end_date.day,
                                  extract('month', User.birthday) <= end_date.month).all()
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int = Path(ge=1), db: Session = Depends(get_db)):
    user = await repository_users.get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(body: UserModel, db: Session = Depends(get_db)):
    user = await repository_users.get_user_by_email(body.email, db)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email is exists!')
    user = await repository_users.create(body, db)
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(body: UserModel, user_id: int = Path(ge=1), db: Session = Depends(get_db)):
    # user = db.query(User).filter_by(id=user_id).first()
    user = await repository_users.update(user_id, body, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user(user_id: int = Path(ge=1), db: Session = Depends(get_db)):
    # user = db.query(User).filter_by(id=user_id).first()
    user = await repository_users.remove(user_id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return user
