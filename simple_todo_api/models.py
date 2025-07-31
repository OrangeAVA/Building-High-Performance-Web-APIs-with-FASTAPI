from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class ToDoItem(Base):
    __tablename__ = "todo_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)  # ✅ Add length
    description = Column(String(1000), nullable=True)  # ✅ Optional length
    completed = Column(Boolean, default=False)
