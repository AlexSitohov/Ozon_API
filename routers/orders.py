from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.orm import Session


from JWT import get_current_user
from schemas import OrderCreate, OrderResponse
import models
from database_config import get_db
from services.make_order_logic import make_order_logic

router = APIRouter(tags=['orders'], prefix='/orders')


@router.post('', status_code=status.HTTP_201_CREATED, response_model=OrderResponse)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    customer_id = current_user.get('user_id')

    result_dict: dict = make_order_logic(customer_id, order_data, db)

    new_order = models.Order(customer_id=customer_id, summa=result_dict.get("summa"),
                             products=result_dict.get("products"))
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


@router.get('/my-orders', response_model=list[OrderResponse])
def get_list_of_my_orders(skip: int = Query(default=0), limit: int = Query(default=10), db: Session = Depends(get_db),
                          current_user=Depends(get_current_user)):
    customer_id = current_user.get('user_id')
    list_of_my_orders = db.query(models.Order).filter(models.Order.customer_id == customer_id).order_by(
        models.Order.id).offset(skip).limit(
        limit).all()
    return list_of_my_orders
