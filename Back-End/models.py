from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    password: str

class UserInDB(User):
    hashed_password: str
    password: Optional[str] = None
    
class Login(BaseModel):
    username: str
    password: str