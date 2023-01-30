import uuid

from fastapi import HTTPException, status
import models


def product_to_order(products_id: list[uuid], db):
    products = []
    summa = 0
    for i in products_id:
        product = db.query(models.Product).filter(models.Product.id == i).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id: {i} not found')
        products.append(product)
        summa += product.price
    return products, summa
