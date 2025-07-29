from pydantic import BaseModel

class ToDoBase(BaseModel):
    title: str
    description: str | None = None

class ToDoCreate(ToDoBase):
    pass

class ToDoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None

class ToDoResponse(ToDoBase):
    id: int
    completed: bool

    class Config:
        orm_mode = True
