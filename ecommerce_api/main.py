from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from models import User, Product, Cart, Wishlist, Order, Review, Coupon
from database import Base, engine
from schemas import UserCreate, UserLogin, Token, ProductCreate, CartItemCreate, ReviewCreate
from dependencies import get_current_user, get_db

from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from fastapi.openapi.utils import get_openapi

# App init and DB setup
app = FastAPI(title="E-commerce API")
Base.metadata.create_all(bind=engine)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT constants
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ------------------ Utility Functions ------------------

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ------------------ Authentication Routes ------------------

@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_admin=True  # 👈 TEMP: for dev/testing only
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User registered successfully"}


@app.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}

# ------------------ Product Routes ------------------

@app.get("/products")
def get_products(search: str = None, min_price: int = 0, max_price: int = 100000, db: Session = Depends(get_db)):
    query = db.query(Product)
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    query = query.filter(Product.price.between(min_price, max_price))
    return query.all()

@app.post("/products")
def add_product(product: ProductCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# ------------------ Cart Routes ------------------

@app.post("/cart")
def add_to_cart(cart_item: CartItemCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == cart_item.product_id).first()
    if not product or product.stock < cart_item.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    existing_item = db.query(Cart).filter(Cart.user_id == user.id, Cart.product_id == cart_item.product_id).first()
    if existing_item:
        existing_item.quantity += cart_item.quantity
    else:
        db_item = Cart(user_id=user.id, **cart_item.dict())
        db.add(db_item)
    db.commit()
    return {"message": "Cart updated"}

@app.get("/cart/{user_id}")
def get_cart(user_id: int, db: Session = Depends(get_db)):
    return db.query(Cart).filter(Cart.user_id == user_id).all()

# ------------------ Wishlist Routes ------------------

@app.post("/wishlist")
def add_to_wishlist(product_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_item = Wishlist(user_id=user.id, product_id=product_id)
    db.add(db_item)
    db.commit()
    return {"message": "Added to wishlist"}

@app.get("/wishlist")
def get_wishlist(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Wishlist).filter(Wishlist.user_id == user.id).all()

# ------------------ Orders ------------------

@app.post("/orders")
def create_order(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cart_items = db.query(Cart).filter(Cart.user_id == user.id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {product.name}")
        product.stock -= item.quantity
        db_order = Order(user_id=user.id, product_id=product.id, quantity=item.quantity, total_price=product.price * item.quantity)
        db.add(db_order)
        db.delete(item)
    db.commit()
    return {"message": "Order placed successfully"}

# ------------------ Reviews ------------------

@app.post("/reviews")
def add_review(review: ReviewCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_review = Review(user_id=user.id, **review.dict())
    db.add(db_review)
    db.commit()
    return {"message": "Review added successfully"}

# ------------------ Coupons ------------------

@app.post("/apply-coupon")
def apply_coupon(code: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    coupon = db.query(Coupon).filter(Coupon.code == code, Coupon.is_active == True).first()
    if not coupon:
        raise HTTPException(status_code=400, detail="Invalid or expired coupon")
    return {"message": f"Coupon applied. {coupon.discount_percentage}% discount available"}

# ------------------ OpenAPI JWT Security ------------------

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="E-commerce API",
        version="1.0.0",
        description="API for an E-commerce Platform with JWT Auth",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
