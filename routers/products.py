from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.orm import Session

from JWT import get_current_user
from schemas import ProductCreate, ProductResponse
import models
from database_config import get_db

router = APIRouter(tags=['products'], prefix='/products')


@router.post('', status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    seller_id = current_user.get('user_id')
    new_product = models.Product(**product_data.dict(), seller_id=seller_id)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.get('', response_model=list[ProductResponse])
def get_products_list(search: str = Query(default=None), skip: int = Query(default=0), limit: int = Query(default=100),
                      db: Session = Depends(get_db)):
    try:
        if search is None:
            products_list = db.query(models.Product).offset(skip).limit(limit).all()
        else:
            products_list = db.query(models.Product).filter(models.Product.title.ilike(f'%{search}%')).offset(skip). \
                limit(limit).all()

        return products_list

    except Exception as exception:
        return {
            'status': status,
            'exception': exception
        }
