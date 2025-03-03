from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List

app = FastAPI()

data = [
    {"id": 1, "name": "Okta"},
    {"id": 2, "name": "Vian"},
    {"id": 3, "name": "Dani"},
    {"id": 4, "name": "Nopal"},
    {"id": 5, "name": "ifa"}
]  # Data dummy untuk contoh

class Item(BaseModel):
    id: int
    name: str

@app.get("/users")
def get_items():
    """Mengambil semua item (200 OK)"""
    return data

@app.get("/users/{item_id}", response_model=Item)
def get_item(item_id: int):
    """Mengambil item berdasarkan ID (200 OK atau 404 Not Found)"""
    for item in data:
        if item["id"] == item_id:
            return Item(**item)  # Mengubah dictionary menjadi objek Item
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/create-users", status_code=201)
def create_item(item: Item):
    """Membuat item baru (201 Created)"""
    if any(existing_item["id"] == item.id for existing_item in data):
        raise HTTPException(status_code=400, detail="Item with this ID already exists")
    if not item.name:
        raise HTTPException(status_code=400, detail="Item name cannot be empty")
    data.append(item.dict())
    return item

@app.put("/edit-users/{item_id}")
def update_item(item_id: int, item: Item):
    """Memperbarui item (200 OK atau 404 Not Found)"""
    for i, existing_item in enumerate(data):
        if existing_item["id"] == item_id:
            data[i] = item.dict()  # Mengubah objek Item menjadi dictionary
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/users/del={item_id}", status_code=200)
def delete_item(item_id: int):
    """Menghapus item berdasarkan ID (200 OK atau 404 Not Found)"""
    for i, item in enumerate(data):
        if item["id"] == item_id:
            del data[i]
            return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/unauthorized")
def unauthorized():
    """Contoh endpoint yang membutuhkan autentikasi (401 Unauthorized)"""
    raise HTTPException(status_code=401, detail="Unauthorized access")

@app.get("/forbidden")
def forbidden():
    """Contoh endpoint yang dilarang diakses (403 Forbidden)"""
    raise HTTPException(status_code=403, detail="Forbidden access")

@app.get("/server-error")
def server_error():
    """Contoh error server (500 Internal Server Error)"""
    raise HTTPException(status_code=500, detail="Internal Server Error")