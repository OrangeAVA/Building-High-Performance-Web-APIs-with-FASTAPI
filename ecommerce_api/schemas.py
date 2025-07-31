from pydantic import BaseModel, EmailStr
from typing import Optional


# ----- User Schemas -----

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_admin: bool

    class Config:
        orm_mode = True


# ----- Product Schemas -----

class ProductCreate(BaseModel):
    name: str
    description: str
    price: int
    stock: int


class ProductOut(BaseModel):
    id: int
    name: str
    description: str
    price: int
    stock: int

    class Config:
        orm_mode = True


# ----- Cart Schemas -----

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int


class CartItemOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int

    class Config:
        orm_mode = True


# ----- Wishlist Schemas -----

class WishlistItem(BaseModel):
    product_id: int


# ----- Review Schemas -----

class ReviewCreate(BaseModel):
    product_id: int
    rating: int
    review_text: Optional[str] = None


# ----- Coupon Schemas -----

class ApplyCoupon(BaseModel):
    code: str
