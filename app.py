from fastapi import FastAPI, Path, HTTPException, Request
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def home():
    return {"Data": "test"}

@app.get("/about")
def about():
    return {"Data": "About"}

inventory = {
    1: {
        "name": "Milk",
        "price": 1.99,
        "type": "skimmed"
    }
}

class Item(BaseModel):
    name: str
    price: float
    type: str

@app.get("/get-item/{item_id}", responses={
    404: {"description": "Item not found"},
    200: {"description": "Successful Response", "content": {"application/json": {}}}
})
def get_item(item_id: int = Path(..., description="The ID of the item you would like to view")):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item not found")
    return inventory[item_id]

@app.post("/add-item/{item_id}", responses={
    400: {"description": "Item ID already exists"},
    200: {"description": "Successful Response", "content": {"application/json": {}}}
})
def add_item(item_id: int, item: Item):
    if item_id in inventory:
        raise HTTPException(status_code=400, detail="Item ID already exists")
    inventory[item_id] = item.dict()
    return inventory[item_id]

@app.get("/get-item", responses={
    200: {"description": "Successful Response", "content": {"application/json": {}}}
})
def get_all_items():
    return inventory
