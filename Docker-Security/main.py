from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
import time

app = FastAPI(title="Secure DevSecOps API")

# Updated Model with an ID for better management
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

# In-memory database
db: List[Item] = []

# Middleware for Security Auditing: Logs request processing time
@app.middleware("http")
async def audit_log_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    # In a real DevSecOps environment, you'd send this to an ELK stack or Splunk
    print(f"Audit: {request.method} {request.url.path} processed in {process_time:.4f}s")
    return response

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.1.0"}

@app.get("/items", response_model=List[Item])
def get_items():
    return db

# New Endpoint: Get a single item by ID
@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    item = next((i for i in db if i.id == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items")
def create_item(item: Item):
    # Check if ID already exists to prevent collisions
    if any(i.id == item.id for i in db):
        raise HTTPException(status_code=400, detail="Item ID already exists")
    db.append(item)
    return {"message": "Item added successfully", "item": item}

# New Endpoint: Delete an item (Essential for CRUD)
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    global db
    initial_length = len(db)
    db = [i for i in db if i.id != item_id]
    if len(db) == initial_length:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": f"Item {item_id} deleted successfully"}

@app.get("/security-info")
def get_security():
    return {
        "user_context": "Running as Non-Root",
        "sandboxing": "Docker Namespaces & Capabilities enabled",
        "logging": "Middleware Audit Enabled"
    }