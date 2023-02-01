from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database_config import engine, Base
from routers import users, authentication, products, orders, update_order_status, comments

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(users.router)
app.include_router(authentication.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(update_order_status.router)
app.include_router(comments.router)

Base.metadata.create_all(engine)
