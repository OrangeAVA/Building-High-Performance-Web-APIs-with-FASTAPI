from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import ToDoItem
from schemas import ToDoCreate, ToDoUpdate
from fastapi import HTTPException

async def create_todo_item(db: AsyncSession, todo: ToDoCreate):
    db_item = ToDoItem(**todo.dict())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

async def get_todo_items(db: AsyncSession):
    result = await db.execute(select(ToDoItem))
    return result.scalars().all()

async def get_todo_item_by_id(db: AsyncSession, item_id: int):
    result = await db.execute(select(ToDoItem).filter(ToDoItem.id == item_id))
    return result.scalars().first()

async def update_todo_item(db: AsyncSession, item_id: int, todo_update: ToDoUpdate):
    db_item = await get_todo_item_by_id(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in todo_update.dict(exclude_unset=True).items():
        setattr(db_item, key, value)
    await db.commit()
    await db.refresh(db_item)
    return db_item

async def delete_todo_item(db: AsyncSession, item_id: int):
    db_item = await get_todo_item_by_id(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    await db.delete(db_item)
    await db.commit()
    return db_item
