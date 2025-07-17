from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import SessionLocal
from models.user import User
from schemas.user_schema import UserCreate, UserLogin, ResetRequest, ResetPassword
from utils.security import hash_password, verify_password, create_access_token, create_reset_token, verify_reset_token
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
    
    # Validar usuario
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Validar contraseña
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    # Validar y retornar token
    token = create_access_token(data={"sub": db_user.username, "user_id": db_user.id})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/reset-password")
def reset_password(data: ResetPassword, db: Session = Depends(get_db)):
    username = verify_reset_token(data.token)
    if not username:
        raise HTTPException(status_code=400, detail="Token inválido o expirado")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user.password = hash_password(data.new_password)
    db.commit()

    return {"message": "Contraseña actualizada correctamente"}


@router.post("/request-password")
def request_password_reset(data: ResetRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Generar token
    token = create_reset_token(user.username)
    # print(f"reseft token {token}")

    # Enviar por email (opcional) o retornar directamente (para pruebas)
    return {"reset_token": token}
