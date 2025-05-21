from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str
    last_name: str
    username: str
    password: str
    agree_terms: bool

class UserLogin(BaseModel):
    username: str
    password: str
    
class UserOut(BaseModel):
    name: str
    last_name: str
    username: str
    password: str
    agree_terms: bool
    
    class Config:
        from_attributes = True
    
class UserUpdate(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None