import uuid

from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Table, Float, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from database_config import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    password = Column(String)
    email = Column(String(30), unique=True)
    phone = Column(Integer, unique=True)
    city = Column(String(30))
    balance = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    is_staff = Column(Boolean, default=False)

    products = relationship('Product', back_populates='seller')

    comments = relationship('Comment', back_populates='commentator')


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    price = Column(Float)
    qty = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

    seller_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

    seller = relationship('User', back_populates='products')

    orders = relationship("Order", secondary="orders_products", back_populates="products")

    comments = relationship('Comment', back_populates='product')


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    summa = Column(Float)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

    status = Column(String, default='Оплачено и скоро будет отправлен')

    products = relationship("Product", secondary="orders_products", back_populates="orders")


orders_products = Table('orders_products', Base.metadata,
                        Column('order_id', ForeignKey('orders.id'), primary_key=True),
                        Column('product_id', ForeignKey('products.id'), primary_key=True)
                        )


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    body = Column(String(200), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

    commentator_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'))

    commentator = relationship('User', back_populates='comments')

    product = relationship('Product', back_populates='comments')
