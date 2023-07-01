from datetime import datetime, date
from pydantic import BaseModel, EmailStr


class UserModel(BaseModel):
    # first_name: str = Field(default="test_f_n")
    first_name: str
    last_name: str
    email: EmailStr
    mobile: str
    birthday: date
    add_info: str


class UserResponse(BaseModel):
    id: int = 1
    first_name: str
    last_name: str
    email: EmailStr
    mobile: str
    birthday: date
    add_info: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
