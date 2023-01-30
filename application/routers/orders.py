from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from JWT import get_current_user
from business_logic import product_to_order
from schemas import OrderCreate, OrderResponse
import models
from database_config import get_db

router = APIRouter(tags=['orders'], prefix='/orders')


@router.post('', status_code=status.HTTP_201_CREATED, response_model=OrderResponse)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    customer_id = current_user.get('user_id')
    customer = db.query(models.User).filter(models.User.id == customer_id).first()

    products_and_sum_price = product_to_order(order_data.products_id, db)

    products = products_and_sum_price[0]
    summa = products_and_sum_price[1]

    if customer.balance < summa:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'не достаточно денег')
    customer.balance -= summa

    new_order = models.Order(customer_id=customer_id, summa=summa, products=products)
    db.commit()
    db.refresh(new_order)
    return new_order


@router.get('/my-orders', response_model=list[OrderResponse])
def get_list_of_my_orders(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    customer_id = current_user.get('user_id')
    list_of_my_orders = db.query(models.Order).filter(models.Order.customer_id == customer_id).all()
    return list_of_my_orders
