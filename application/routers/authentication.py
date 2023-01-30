from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from hash import verify_password
import models
from database_config import get_db
from JWT import create_access_token

router = APIRouter(tags=['authentication'])


@router.post('/login', status_code=status.HTTP_200_OK)
def login(login_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == login_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not correct')
    if not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not correct')
    access_token = create_access_token(data={'user_id': user.id,
                                             'username': user.username,
                                             'is_staff': user.is_staff,
                                             'user_email': user.email}, )

    return {"access_token": access_token, "token_type": "bearer"}
