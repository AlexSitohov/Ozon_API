from fastapi import APIRouter, status, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from JWT import get_current_user
from schemas import OrderResponse, OrderUpdate
import models
from database_config import get_db
from services.send_mail import create_background_task

router = APIRouter(tags=['update_order_status'], prefix='/update-order-status')


@router.patch('', response_model=OrderResponse)
def update_order_status(background_tasks: BackgroundTasks, order_update_data: OrderUpdate,
                        db: Session = Depends(get_db),
                        current_user=Depends(get_current_user)):
    user_is_staff = current_user.get('is_staff')
    if not user_is_staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'нет доступа')

    update_order = db.query(models.Order).filter(models.Order.id == order_update_data.id)
    order = update_order.first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404,
                            detail=f'order with id: {order_update_data} not exists')
    order.status = order_update_data.status
    db.commit()
    db.refresh(order)
    user = db.query(models.User).filter(models.User.id == order.customer_id).first()
    create_background_task(background_tasks, user, order)
    return order
