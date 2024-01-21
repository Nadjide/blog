import sqlite3
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
import bcrypt
from datetime import datetime, timedelta
import secrets
from models import User, UserInDB, Login

def create_secret_key():
    return secrets.token_hex(32)

SECRET_KEY = create_secret_key()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

app = FastAPI()

def get_db():
    conn = sqlite3.connect('blog.db')
    return conn

def hash_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def save_user(user: User):
    conn = get_db()
    c = conn.cursor()
    hashed_password = hash_password(user.password)
    c.execute("INSERT INTO User (username, email, password) VALUES (?, ?, ?)",
              (user.username, user.email, hashed_password))
    conn.commit()
    return UserInDB(**user.dict(), hashed_password=hashed_password)

def get_user(username: str):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM User WHERE username=?", (username,))
    user = c.fetchone()
    if user is None:
        return None
    return UserInDB(username=user[1], email=user[2], hashed_password=user[3])

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Routes
@app.get('/')
def index():
    return "Hello World!"

@app.post("/register", response_model=UserInDB)
def register(user: User):
    return save_user(user)

@app.post("/login")
def login(login_data: Login):
    user = get_user(login_data.username)
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}