# Social Media API - FastAPI

A fully-functional social media backend API built with FastAPI and SQLAlchemy, featuring JWT-based authentication.

---

## 🚀 Features

- ✅ User registration & login with JWT auth
- 📝 Create, fetch user posts
- ❤️ Like posts and 💬 comment on them
- 🔔 Receive and view notifications
- 🤝 Friend request system (send/accept)
- 🔐 Protected routes using JWT
- 📄 Swagger documentation with built-in token authorization

---

## 🛠️ Tech Stack

- Python 3.10+
- FastAPI
- SQLAlchemy
- SQLite/MySQL/PostgreSQL
- JWT (via `python-jose`)
- Alembic (optional, for DB migrations)

---
## Folder Structure

social-media-api/
│
├── main.py
├── models.py
├── schemas.py
├── database.py
├── dependencies.py
├── utils.py
├── requirements.txt
└── README.md


## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/girishvas/Building-High-Performance-Web-APIs-with-FAST-API.git
cd social-media-api

python3 -m venv env
source env/bin/activate

pip install -r requirements.txt

uvicorn main:app --reload

http://127.0.0.1:8000/docs

alembic init alembic
# update alembic/env.py and alembic.ini
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
