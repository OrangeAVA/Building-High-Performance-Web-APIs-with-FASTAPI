# 📝 Simple To-Do API (FastAPI + MySQL + Async SQLAlchemy + Alembic)

This is a fully asynchronous To-Do List API built using **FastAPI**, **MySQL**, **SQLAlchemy 2.0 (async)**, and **Alembic** for database migrations.

---

## 🚀 Features

- ✅ Fully async FastAPI backend
- ✅ MySQL database with async SQLAlchemy support
- ✅ Pydantic-based request & response validation
- ✅ CRUD operations (Create, Read, Update, Delete)
- ✅ Alembic for schema migrations
- ✅ Modular project structure

---

## 🧱 Tech Stack

| Component       | Tech                             |
|----------------|-----------------------------------|
| Framework      | [FastAPI](https://fastapi.tiangolo.com) |
| ORM            | [SQLAlchemy 2.0 (async)](https://docs.sqlalchemy.org/en/20/) |
| Database       | MySQL 8+                          |
| Driver         | `aiomysql` (async), `pymysql` (for Alembic) |
| Migrations     | [Alembic](https://alembic.sqlalchemy.org/) |
| Python Version | 3.12+                             |

---

## 📁 Project Structure
simple_todo_api/
├── main.py # FastAPI app + route setup
├── models.py # SQLAlchemy models
├── crud.py # Business logic / DB operations
├── schemas.py # Pydantic models
├── database.py # DB engine + session
├── alembic/ # Alembic migration scripts
│ └── versions/
├── alembic.ini # Alembic config
└── README.md

## ⚙️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/simple-todo-api.git
cd simple-todo-api

python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt

DATABASE_URL = "mysql+aiomysql://user:password@localhost:3306/todo_db"

# Create new migration
alembic init alembic

alembic revision --autogenerate -m "initial"

# Apply all migrations
alembic upgrade head

alembic revision --autogenerate -m "create todo_items table"
alembic upgrade head

# Rollback last migration
alembic downgrade -1
