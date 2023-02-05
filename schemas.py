import re

from datetime import datetime

from fastapi import HTTPException, status

from pydantic import BaseModel, validator, Field

LETTER_MATCH_PATTERN = re.compile(r"^[a-zA-Z\-]+$")


class UserCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str
    email: str
    phone: str
    city: str
    balance: int = Field(gt=0, lt=1_000_000)

    @validator("username")
    def validate_username(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="username should contains only letters"
            )
        return value

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    password: str
    email: str
    phone: str
    city: str
    created_at: datetime
    balance: int

    class Config:
        orm_mode = True


class UserResponsePartial(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class ProfileResponse(UserResponse):
    class Config:
        orm_mode = True


class ProfileUpdate(BaseModel):
    username: str
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class PasswordChange(BaseModel):
    old_password: str
    new_password: str


class ProductCreate(BaseModel):
    title: str
    price: float
    qty: int

    class Config:
        orm_mode = True


class CommentsResponseProduct(BaseModel):
    id: int
    body: str

    product_id: int

    commentator: UserResponsePartial

    class Config:
        orm_mode = True


class ProductResponse(BaseModel):
    id: int
    title: str
    price: float
    qty: int
    seller_id: int
    created_at: datetime
    comments: list[CommentsResponseProduct]

    class Config:
        orm_mode = True


class OrderCreate(BaseModel):
    products_id: list[int]


class OrderResponse(BaseModel):
    id: int
    customer_id: int
    created_at: datetime
    summa: float
    status: str
    products: list[ProductResponse]

    class Config:
        orm_mode = True


class OrderUpdate(BaseModel):
    id: int
    status: str

    class Config:
        orm_mode = True


class CommentsCreate(BaseModel):
    body: str
    product_id: int

    class Config:
        orm_mode = True


class CommentsResponse(BaseModel):
    id: int
    body: str
    created_at: datetime

    product_id: int

    commentator: UserResponsePartial

    class Config:
        orm_mode = True
