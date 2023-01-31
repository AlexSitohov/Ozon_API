from fastapi import HTTPException, status, Depends
from database_config import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func as generic_function
import models


def make_order_logic(customer_id, order_data, db: Session = Depends(get_db)):
    """
    :param customer_id: id пользователя
    :param order_data: id товаров  для создания заказа
    :param db: ...
    :return: ...
    """
    # Получаем информацию о пользователе. На 33 строке изменяем у него баланс.
    customer = db.query(models.User).filter(models.User.id == customer_id).first()

    # Получаем информацию о товарах, также получаем сумму всех цен товаров в summa.
    products_summa = db.query(models.Product, generic_function.sum(models.Product.price).label('summa')).group_by(
        models.Product.id).filter(
        models.Product.id.in_(order_data.products_id)).all()

    # В summa записываем сумму всех цен товаров, а в products сами продукты.
    summa = sum([i[1] for i in products_summa])
    products = [i[0] for i in products_summa]

    # Проверяем хватает ли у пользователя денег на счету для оплаты. Если нет, то вызываем исключение.
    if customer.balance < summa:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'не достаточно денег')
    # Обновляем количество у каждого товара.
    db.query(models.Product).filter(
        models.Product.id.in_(order_data.products_id)).update({models.Product.qty: models.Product.qty - 1},
                                                              synchronize_session='evaluate')
    # Снимаем деньги с баланса пользователя.
    customer.balance -= summa

    return {
        "summa": summa,
        "products": products
    }
