from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from models import User, Post, Like, Comment, Notification, Friendship
from database import Base, engine
from schemas import UserCreate, UserLogin, Token, PostCreate, CommentCreate
from dependencies import get_current_user, get_db

from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from fastapi.openapi.utils import get_openapi

app = FastAPI(title="Social Media API")
Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
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

@app.get("/users/me")
def get_current_user_profile(user: User = Depends(get_current_user)):
    return user

@app.post("/posts")
def create_post(post: PostCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_post = Post(user_id=user.id, **post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@app.get("/posts")
def get_user_posts(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Post).filter(Post.user_id == user.id).all()

@app.get("/posts/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.put("/posts/{post_id}")
def update_post(post_id: int, post: PostCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_post = db.query(Post).get(post_id)
    if not db_post or db_post.user_id != user.id:
        raise HTTPException(status_code=403, detail="Permission denied")
    for key, value in post.dict().items():
        setattr(db_post, key, value)
    db.commit()
    return db_post

@app.delete("/posts/{post_id}")
def delete_post(post_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_post = db.query(Post).get(post_id)
    if not db_post or db_post.user_id != user.id:
        raise HTTPException(status_code=403, detail="Permission denied")
    db.delete(db_post)
    db.commit()
    return {"message": "Post deleted"}

@app.post("/like")
def like_post(post_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    like = Like(user_id=user.id, post_id=post_id)
    db.add(like)
    db.commit()
    return {"message": "Post liked"}

@app.delete("/like/{post_id}")
def unlike_post(post_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_like = db.query(Like).filter_by(user_id=user.id, post_id=post_id).first()
    if db_like:
        db.delete(db_like)
        db.commit()
    return {"message": "Unliked"}

@app.get("/likes/{post_id}")
def get_post_likes(post_id: int, db: Session = Depends(get_db)):
    return db.query(Like).filter_by(post_id=post_id).all()

@app.post("/comment")
def comment_on_post(post_id: int, comment: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_comment = Comment(user_id=user.id, post_id=post_id, comment=comment)
    db.add(db_comment)
    db.commit()
    return db_comment

@app.get("/comments/{post_id}")
def get_post_comments(post_id: int, db: Session = Depends(get_db)):
    return db.query(Comment).filter_by(post_id=post_id).all()

@app.put("/comment/{comment_id}")
def edit_comment(comment_id: int, comment_data: CommentCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    comment = db.query(Comment).get(comment_id)
    if not comment or comment.user_id != user.id:
        raise HTTPException(status_code=403, detail="Permission denied")
    comment.comment = comment_data.comment
    db.commit()
    return comment

@app.delete("/comment/{comment_id}")
def delete_comment(comment_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    comment = db.query(Comment).get(comment_id)
    if not comment or comment.user_id != user.id:
        raise HTTPException(status_code=403, detail="Permission denied")
    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted"}

@app.get("/notifications")
def get_notifications(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Notification).filter_by(user_id=user.id).all()

@app.put("/notifications/{notification_id}/read")
def mark_notification_read(notification_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    notif = db.query(Notification).get(notification_id)
    if notif and notif.user_id == user.id:
        notif.is_read = True
        db.commit()
    return {"message": "Marked as read"}

@app.delete("/notifications/{notification_id}")
def delete_notification(notification_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    notif = db.query(Notification).get(notification_id)
    if notif and notif.user_id == user.id:
        db.delete(notif)
        db.commit()
    return {"message": "Notification deleted"}

@app.post("/friend-request")
def send_friend_request(friend_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_request = Friendship(user1_id=user.id, user2_id=friend_id, status="pending")
    db.add(db_request)
    db.commit()
    return {"message": "Friend request sent"}

@app.get("/friend-requests")
def get_friend_requests(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Friendship).filter_by(user2_id=user.id, status="pending").all()

@app.post("/accept-friend-request")
def accept_friend_request(request_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    req = db.query(Friendship).get(request_id)
    if not req or req.user2_id != user.id:
        raise HTTPException(status_code=403, detail="Permission denied")
    req.status = "accepted"
    db.commit()
    return {"message": "Friend request accepted"}

@app.post("/reject-friend-request")
def reject_friend_request(request_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    req = db.query(Friendship).get(request_id)
    if not req or req.user2_id != user.id:
        raise HTTPException(status_code=403, detail="Permission denied")
    req.status = "rejected"
    db.commit()
    return {"message": "Friend request rejected"}

@app.delete("/friends/{friend_id}")
def unfriend(friend_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    friendship = db.query(Friendship).filter(
        ((Friendship.user1_id == user.id) & (Friendship.user2_id == friend_id)) |
        ((Friendship.user1_id == friend_id) & (Friendship.user2_id == user.id))
    ).first()
    if friendship:
        db.delete(friendship)
        db.commit()
    return {"message": "Unfriended"}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Social Media API",
        version="1.0.0",
        description="API for a Social Media Platform with JWT Auth",
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
