from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from database_config import get_db
from JWT import get_current_user
import models
from hash import verify_password, hash
from schemas import ProfileUpdate, ProfileResponse, PasswordChange

router = APIRouter(prefix='/profiles', tags=['profiles'])


@router.get('', status_code=status.HTTP_200_OK, response_model=ProfileResponse)
def get_my_profile_data(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    user_id = current_user.get('user_id')
    my_profile_data = db.query(models.User).filter(models.User.id == user_id).first()
    return my_profile_data


@router.put('', status_code=status.HTTP_200_OK, response_model=ProfileResponse)
def update_profile_data(profile_data: ProfileUpdate, db: Session = Depends(get_db),
                        current_user=Depends(get_current_user)):
    user_id = current_user.get('user_id')
    my_profile_data_query = db.query(models.User).filter(models.User.id == user_id)

    my_profile_data = my_profile_data_query.first()

    my_profile_data_query.update(
        {models.User.username: profile_data.username,
         models.User.first_name: profile_data.first_name,
         models.User.last_name: profile_data.last_name})
    db.commit()
    db.refresh(my_profile_data)
    return my_profile_data


@router.patch('/change-password', status_code=status.HTTP_200_OK)
def change_password(password_change_data: PasswordChange, db: Session = Depends(get_db),
                    current_user=Depends(get_current_user)):
    user_id = current_user.get('user_id')
    user_change_password = db.query(models.User).filter(models.User.id == user_id).first()
    if not verify_password(password_change_data.old_password, user_change_password.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not correct')
    hashed_password = hash(password_change_data.new_password)
    user_change_password.password = hashed_password
    db.commit()
    db.refresh(user_change_password)
    return {'msg': 'Ваш пароль изменен'}
