import sqlite3
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
import bcrypt
from datetime import datetime, timedelta
import secrets
from models import Article, Comment, User, UserInDB, Login
from typing import List


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

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    conn = sqlite3.connect("blog.db")
    return conn


def hash_password(password: str):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def save_user(user: User):
    conn = get_db()
    c = conn.cursor()
    hashed_password = hash_password(user.password)
    c.execute(
        "INSERT INTO User (username, email, password) VALUES (?, ?, ?)",
        (user.username, user.email, hashed_password),
    )
    conn.commit()
    user_id = c.lastrowid
    return UserInDB(**user.model_dump(), id=user_id, hashed_password=hashed_password)


def get_user(username: str):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM User WHERE username=?", (username,))
    user = c.fetchone()
    if user is None:
        return None
    return UserInDB(id=user[0], username=user[1], email=user[2], hashed_password=user[3])


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
@app.get("/")
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
    return {
        "access_token": access_token, 
        "token_type": "bearer", 
        "username": user.username, 
        "id": user.id
    }

@app.post("/logout")
def logout():
    return {"message": "Logout successful"}

@app.post("/articles", response_model=Article)
def create_article(article: Article):
    conn = get_db()
    c = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute(
        "INSERT INTO Articles (title, author, content, slug, date, user_id) VALUES (?, ?, ?, ?, ?, ?)",
        (article.title, article.author, article.content, article.slug, date, article.user_id),
    )
    conn.commit()
    article_dict = article.model_dump()
    article_dict.pop('id', None)
    return Article(**article_dict, id=c.lastrowid)

@app.get("/articles", response_model=List[Article])
def get_articles():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM Articles")
    articles = c.fetchall()
    articles_list = []
    for article in articles:
        article_dict = {"id": article[0], "title": article[1], "author": article[2], "content": article[3], "slug": article[4], "date": article[5], "user_id": article[6]}
        articles_list.append(Article(**article_dict))
    return articles_list

@app.get("/articles/{article_id}", response_model=Article)
def get_article(article_id: int):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM Articles WHERE id=?", (article_id,))
    article_tuple = c.fetchone()
    if article_tuple is None:
        raise HTTPException(status_code=404, detail="Article not found")
    article_dict = {"id": article_tuple[0], "title": article_tuple[1], "author": article_tuple[2], "content": article_tuple[3], "slug": article_tuple[4], "date": article_tuple[5], "user_id": article_tuple[6]}
    return Article(**article_dict)

@app.delete("/articles/{article_id}")
def delete_article(article_id: int):
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM Articles WHERE id=?", (article_id,))
    conn.commit()
    if c.rowcount == 0:
        raise HTTPException(status_code=404, detail="Article not found")
    return {"message": "Article deleted successfully"}

@app.put("/articles/{article_id}", response_model=Article)
def update_article(article_id: int, article: Article):
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "UPDATE Articles SET title=?, author=?, content=?, slug=?, date=?, user_id=? WHERE id=?",
        (article.title, article.author, article.content, article.slug, article.date, article.user_id, article_id),
    )
    conn.commit()
    if c.rowcount == 0:
        raise HTTPException(status_code=404, detail="Article not found")
    article_dict = article.model_dump()
    if 'id' in article_dict:
        del article_dict['id']
    return Article(**article_dict, id=article_id)

@app.post("/articles/{article_id}/comments", response_model=Comment)
def create_comment(article_id: int, comment: Comment):
    conn = get_db()
    c = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute(
        "INSERT INTO Comments (content, date, user_id, article_id) VALUES (?, ?, ?, ?)",
        (comment.content, date, comment.user_id, article_id),
    )
    conn.commit()
    if c.rowcount == 0:
        raise HTTPException(status_code=404, detail="Article not found")
    comment_dict = comment.model_dump()
    comment_dict['id'] = c.lastrowid
    return Comment(**comment_dict)

@app.get("/articles/{article_id}/comments", response_model=List[Comment])
def get_comments(article_id: int):
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        SELECT Comments.id, Comments.content, Comments.date, Comments.user_id, Comments.article_id, User.username 
        FROM Comments 
        JOIN User ON Comments.user_id = User.id 
        WHERE Comments.article_id=?
    """, (article_id,))
    comments = c.fetchall()
    comments_list = []
    for comment in comments:
        comment_dict = {"id": comment[0], "content": comment[1], "date": comment[2], "user_id": comment[3], "article_id": comment[4], "username": comment[5]}
        comments_list.append(Comment(**comment_dict))
    return comments_list

@app.get("/articles/{article_id}/comments/{comment_id}", response_model=Comment)
def get_comment(article_id: int, comment_id: int):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM Comments WHERE article_id=? AND id=?", (article_id, comment_id))
    comment_tuple = c.fetchone()
    if comment_tuple is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    comment_dict = {"id": comment_tuple[0], "content": comment_tuple[1], "date": comment_tuple[2], "user_id": comment_tuple[3], "article_id": comment_tuple[4]}
    return Comment(**comment_dict)

@app.delete("/articles/{article_id}/comments/{comment_id}")
def delete_comment(article_id: int, comment_id: int):
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM Comments WHERE article_id=? AND id=?", (article_id, comment_id))
    conn.commit()
    if c.rowcount == 0:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"message": "Comment deleted successfully"}

@app.put("/articles/{article_id}/comments/{comment_id}", response_model=Comment)
def update_comment(article_id: int, comment_id: int, comment: Comment):
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "UPDATE Comments SET content=?, date=?, user_id=?, article_id=? WHERE id=?",
        (comment.content, comment.date, comment.user_id, article_id, comment_id),
    )
    conn.commit()
    if c.rowcount == 0:
        raise HTTPException(status_code=404, detail="Comment not found")
    return Comment(**comment.model_dump(), id=comment_id)

@app.get("/articles/search/{title}", response_model=List[Article])
def search_articles(title: str):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM Articles WHERE title LIKE ?", ('%'+title+'%',))
    articles = c.fetchall()
    articles_list = []
    for article in articles:
        article_dict = {"id": article[0], "title": article[1], "author": article[2], "content": article[3], "slug": article[4], "date": article[5], "user_id": article[6]}
        articles_list.append(Article(**article_dict))
    return articles_list