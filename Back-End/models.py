from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    password: str

class UserInDB(BaseModel):
    id: int
    username: str
    hashed_password: str
    
class Login(BaseModel):
    id: Optional[int] = None
    username: str
    password: str

class Article(BaseModel):
    id: Optional[int] = None
    title: str
    author: str
    content: str
    slug: str
    date: Optional[str] = None
    user_id: Optional[int] = None
    
class Comment(BaseModel):    
    id: Optional[int] = None
    content: str
    date: Optional[str] = None
    user_id: Optional[int] = None
    article_id: Optional[int] = None
    username: Optional[str] = None
    
    class config:
        orm_mode = True