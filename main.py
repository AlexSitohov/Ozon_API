import random
import asyncio

from string import ascii_letters

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from database_config import Base, engine
from routers import users, authentication, products, orders, update_order_status, comments, profiles

from fastapi.responses import HTMLResponse
from config import HOST

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
app.include_router(profiles.router)

Base.metadata.create_all(engine)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>websocket</title>
    </head>
    <body>
        <h1>WebSocket</h1>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://62.113.102.58/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print('Accepting client connection...')
    await websocket.accept()
    while True:
        try:
            res = ''.join(random.sample(ascii_letters, random.randint(1, 30)))
            await websocket.send_json(str(res))
            await asyncio.sleep(2)
        except Exception as e:
            print('error:', e)
            break
    print('Bye..')
