# 🛒 E-commerce API using FastAPI

A complete backend API for an E-commerce platform built using **FastAPI**, **SQLAlchemy**, and **JWT authentication**. This API supports user registration, login, product management, cart, wishlist, order processing, reviews, and coupon-based discounts.

---

## 🚀 Features

- ✅ User Signup and Login with JWT
- 🛍 Product Listing, Creation (Admin only)
- 🛒 Cart and Wishlist Management
- 📦 Order Placement with Stock Check
- ⭐ Product Reviews and Ratings
- 🎟 Apply Coupons for Discounts
- 🧪 Unit test structure included

---

## 🗂️ Project Structure

ecommerce_api/
├── main.py # API entry point
├── models.py # SQLAlchemy models
├── schemas.py # Pydantic schemas
├── crud.py # (Optional) Reusable DB ops
├── database.py # DB connection/session
├── dependencies.py # Dependency injection (auth/session)
├── tests/ # Unit/integration tests
│ ├── test_products.py
│ ├── test_orders.py
└── requirements.txt # Python dependencies


---

## ⚙️ Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) — Web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM
- [Pydantic](https://pydantic-docs.helpmanual.io/) — Data validation
- [Uvicorn](https://www.uvicorn.org/) — ASGI server
- [Passlib](https://passlib.readthedocs.io/en/stable/) — Password hashing
- [PyJWT](https://pyjwt.readthedocs.io/) via `python-jose` — JWT handling

---

## 🧑‍💻 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/Building-High-Performance-Web-APIs-with-FAST-API.git
cd Building-High-Performance-Web-APIs-with-FAST-API/ecommerce_api


python3 -m venv env
source env/bin/activate

pip install -r requirements.txt

alembic revision --autogenerate -m "initial"
alembic upgrade head

uvicorn main:app --reload

pytest tests/

