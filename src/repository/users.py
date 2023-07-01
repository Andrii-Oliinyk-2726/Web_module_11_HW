from sqlalchemy.orm import Session

from src.schemas import UserResponse, UserModel
from src.database.models import User


async def get_users(db: Session):
    users = db.query(User).all()
    return users


async def get_user_by_id(user_id: int, db: Session):
    user = db.query(User).filter_by(id=user_id).first()
    return user


async def get_user_by_email(email: str, db: Session):
    user = db.query(User).filter_by(email=email).first()
    return user


async def create(body: UserModel, db: Session):
    user = User(**body.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def update(user_id: int, body: UserModel, db: Session):
    user = await get_user_by_id(user_id, db)
    if user:
        user.first_name = body.first_name
        user.last_name = body.last_name
        user.email = body.email
        user.mobile = body.mobile
        user.birthday = body.birthday
        user.add_info = body.add_info
        db.commit()
    return user


async def remove(user_id: int, db: Session):
    user = await get_user_by_id(user_id, db)
    if user:
        db.delete(user)
        db.commit()
    return user

