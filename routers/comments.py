from fastapi import APIRouter, status, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from JWT import get_current_user
from schemas import CommentsCreate, CommentsResponse
import models
from database_config import get_db

router = APIRouter(tags=['comments'], prefix='/comments')


@router.post('', status_code=status.HTTP_201_CREATED, response_model=CommentsResponse)
def create_comment(comment_data: CommentsCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    commentator_id = current_user.get('user_id')
    new_comment = models.Comment(**comment_data.dict(), commentator_id=commentator_id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@router.get('/my-comments', status_code=status.HTTP_201_CREATED, response_model=list[CommentsResponse])
def get_list_of_my_comments(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    commentator_id = current_user.get('user_id')
    list_of_my_comments = db.query(models.Comment).filter(models.Comment.commentator_id == commentator_id).all()
    return list_of_my_comments


@router.delete('/{comment_id}')
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    commentator_id = current_user.get('user_id')

    comment_to_delete_query = db.query(models.Comment).filter(models.Comment.id == comment_id)
    comment_to_delete = comment_to_delete_query.first()

    if not comment_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'комментарий с id: {comment_id} не найден.')

    if comment_to_delete.commentator_id != commentator_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='нет доступа')

    comment_to_delete_query.delete()
    db.commit()
    return comment_to_delete
