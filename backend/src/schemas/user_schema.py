from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    last_name: str
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str