from sqlalchemy.orm import Session
from models import User, Product, Cart, Wishlist, Order, Review, Coupon
from schemas import UserCreate, ProductCreate, CartItemCreate, ReviewCreate
from passlib.context import CryptContext
from fastapi import HTTPException


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ----- User CRUD -----

def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_admin=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not pwd_context.verify(password, user.hashed_password):
        return None
    return user


# ----- Product CRUD -----

def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_products(db: Session, search: str = None, min_price: int = 0, max_price: int = 100000):
    query = db.query(Product)
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    query = query.filter(Product.price.between(min_price, max_price))
    return query.all()


# ----- Cart CRUD -----

def add_to_cart(db: Session, user_id: int, item: CartItemCreate):
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product or product.stock < item.quantity:
        raise HTTPException(status_code=400, detail="Invalid or insufficient stock")

    cart_item = db.query(Cart).filter(Cart.user_id == user_id, Cart.product_id == item.product_id).first()
    if cart_item:
        cart_item.quantity += item.quantity
    else:
        cart_item = Cart(user_id=user_id, **item.dict())
        db.add(cart_item)
    db.commit()
    return cart_item


def get_cart(db: Session, user_id: int):
    return db.query(Cart).filter(Cart.user_id == user_id).all()


# ----- Wishlist CRUD -----

def add_to_wishlist(db: Session, user_id: int, product_id: int):
    wishlist_item = Wishlist(user_id=user_id, product_id=product_id)
    db.add(wishlist_item)
    db.commit()
    return wishlist_item


def get_wishlist(db: Session, user_id: int):
    return db.query(Wishlist).filter(Wishlist.user_id == user_id).all()


# ----- Review CRUD -----

def create_review(db: Session, user_id: int, review: ReviewCreate):
    db_review = Review(user_id=user_id, **review.dict())
    db.add(db_review)
    db.commit()
    return db_review


# ----- Coupon CRUD -----

def apply_coupon(db: Session, code: str):
    coupon = db.query(Coupon).filter(Coupon.code == code, Coupon.is_active == True).first()
    if not coupon:
        raise HTTPException(status_code=400, detail="Invalid or expired coupon")
    return coupon
