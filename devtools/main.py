from fastapi import FastAPI
from pydantic import BaseModel

# Create virtual environment and install FastAPI and Uvicorn
# Currently gitignoring __pycache__ and virtual environment named test

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None

# GET request at the root endpoint
@app.get("/")
def read_root():
    return {"Hello": "World"}

# GET request with a path parameter and an optional query parameter
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

# PUT request to update an item with a path parameter and a request body
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}