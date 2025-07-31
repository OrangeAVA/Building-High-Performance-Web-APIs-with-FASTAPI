from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import Base, engine, get_db
from schemas import ToDoCreate, ToDoResponse, ToDoUpdate
from crud import create_todo_item, get_todo_items, get_todo_item_by_id, update_todo_item, delete_todo_item

app = FastAPI(
    title="Simple To-Do API",
    description="A minimal async FastAPI app with CRUD features and MySQL/PostgreSQL support.",
    version="1.0.0",
    docs_url="/swagger",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Create database tables on startup
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Create To-Do item
@app.post("/todos/", response_model=ToDoResponse)
async def add_todo(todo: ToDoCreate, db: AsyncSession = Depends(get_db)):
    return await create_todo_item(db, todo)

# List all To-Do items
@app.get("/todos/", response_model=list[ToDoResponse])
async def list_todos(db: AsyncSession = Depends(get_db)):
    return await get_todo_items(db)

# Get single To-Do item
@app.get("/todos/{item_id}/", response_model=ToDoResponse)
async def get_todo(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await get_todo_item_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Update To-Do item
@app.put("/todos/{item_id}/", response_model=ToDoResponse)
async def modify_todo(item_id: int, todo_update: ToDoUpdate, db: AsyncSession = Depends(get_db)):
    return await update_todo_item(db, item_id, todo_update)

# Delete To-Do item
@app.delete("/todos/{item_id}/", response_model=ToDoResponse)
async def remove_todo(item_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_todo_item(db, item_id)
