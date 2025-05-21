from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import SessionLocal
from models.user import User
from schemas.user_schema import UserOut, UserUpdate, UserPasswordUpdate
from utils.security import hash_password
from typing import List
from utils.security import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# Dependency para obtener la sesión de la DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[UserOut])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.get("/me", response_model=UserOut)
def get_my_user(current_user: UserOut = Depends(get_current_user)):
    return current_user

@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if user_update.name is not None:
        user.name = user_update.name
    if user_update.last_name is not None:
        user.last_name = user_update.last_name
    if user_update.phone is not None:
        user.phone = user_update.phone
    if user_update.specialty is not None:
        user.specialty = user_update.specialty 

    db.commit()
    db.refresh(user)
    return user

@router.put("/password/{user_id}", response_model=UserOut)
def update_user(user_id: int, user_pass_update: UserPasswordUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if user_pass_update.password is not None:
        user.password = user_pass_update.password 

    db.commit()
    db.refresh(user)
    return user

# ------------------------------------IMPORTANTE------------------------------------------
# Validar que solo un usuario logueado pueda realizar cambios sobre los datos desde la API