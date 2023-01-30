from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func as generic_function

from JWT import get_current_user
from schemas import OrderCreate, OrderResponse
import models
from database_config import get_db

router = APIRouter(tags=['orders'], prefix='/orders')


@router.post('', status_code=status.HTTP_201_CREATED, response_model=OrderResponse)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    customer_id = current_user.get('user_id')
    customer = db.query(models.User).filter(models.User.id == customer_id).first()

    products_summa = db.query(models.Product, generic_function.sum(models.Product.price).label('summa')).group_by(
        models.Product.id).filter(
        models.Product.id.in_(order_data.products_id)).all()

    summa = sum([i[1] for i in products_summa])
    products = [i[0] for i in products_summa]

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
