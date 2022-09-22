# uvicorn main:app --reload
from ctypes import Union
import string
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

class Order(BaseModel):
  id: int
  name: str
  description: str
  price: float
  tax: float

app = FastAPI()

class ConnectionManager:
  def __init__(self):
    self.active_connections: List[WebSocket] = []

  async def connect(self, websocket: WebSocket):
    await websocket.accept()
    self.active_connections.append(websocket)

  def disconnect(self, websocket: WebSocket):
    self.active_connections.remove(websocket)

  async def send_personal_message(self, message: str, websocket: WebSocket):
    await websocket.send_text(message)

  async def broadcast(self, message: str):
    for connection in self.active_connections:
      await connection.send_text(message)


manager = ConnectionManager()
ordens = []


async def notifications(qtd: string):
  await manager.broadcast(qtd)


@app.on_event("startup")
async def startup_event():
  order =  Order(
    id = 1,
    name = "Meu nome",
    description = "Essa descrição é massa",
    price = 3.9,
    tax = 3
  )
  ordens.append(order)
  print("Iniciei", ordens)

    
@app.post("/append/")
async def create_order(order: Order):
  ordens.append(order)
  print("append", ordens)
  await notifications(f"{len(ordens)}")

@app.delete("/remove/{id}")
async def del_order(id: int):

  for index, ordem in enumerate(ordens):
    if ordem.id == id:
      del(ordens[index])

  print("del", ordens)

  await notifications(f"{len(ordens)}")


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
  try:
    await manager.connect(websocket)
    while True:
      await manager.broadcast(f"{len(ordens)}")
      await websocket.receive_text()
  except WebSocketDisconnect:
    manager.disconnect(websocket)
    # await manager.broadcast(f"Client #{client_id} left the chat")