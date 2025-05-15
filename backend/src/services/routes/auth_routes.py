from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import SessionLocal
from models.user import User
from schemas.user_schema import UserCreate, UserLogin
from utils.security import hash_password, verify_password, create_access_token
from fastapi import Query

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# Dependency para obtener la sesión de la DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Verificar si el usuario ya existe
    user_exist = db.query(User).filter(User.username == user_data.username).first()
    if user_exist:
        raise HTTPException(status_code=409, detail="El usuario ya existe")

    # Hashear la contraseña y crear el nuevo usuario
    hashed_pass = hash_password(user_data.password)
    new_user = User(
        name=user_data.name,
        last_name = user_data.last_name,
        username=user_data.username,
        password=hashed_pass
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Usuario registrado correctamente"}

@router.get("/check-username")
def check_username(username: str = Query(...), db: Session = Depends(get_db)):
    """
    Devuelve {"exists": true} si ya hay un usuario con ese username,
    o {"exists": false} si está libre.
    """
    exists = db.query(User).filter(User.username == username).first() is not None
    return {"exists": exists}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    
    # Validar existencia y contraseña
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    # Generar y retornar el token
    token = create_access_token(data={"sub": db_user.username, "user_id": db_user.id})
    return {"access_token": token, "token_type": "bearer"}
