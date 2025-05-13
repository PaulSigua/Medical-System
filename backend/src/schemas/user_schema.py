from pydantic import BaseModel

class UserCreate(BaseModel):
    nombre: str
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str