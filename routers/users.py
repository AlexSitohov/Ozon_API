from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from schemas import UserCreate, UserResponse
import models
from database_config import get_db
from hash import hash

router = APIRouter(tags=['users'], prefix='/users')


@router.post('', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def register_user(user_date: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash(user_date.password)
    user_date.password = hashed_password
    new_user = models.User(**user_date.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('', response_model=list[UserResponse])
def get_users_list(db: Session = Depends(get_db)):
    try:
        users_list = db.query(models.User).all()
        return users_list
    except Exception as exception:
        return {
            'status': status,
            'exception': exception
        }
