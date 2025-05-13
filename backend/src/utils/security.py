import bcrypt
import os
from jose import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()
# Obtener la ruta del archivo .env
env_path = os.path.join(os.path.dirname(__file__), '..', 'services', '.env')
load_dotenv(dotenv_path=os.path.abspath(env_path))

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=2)):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + expires_delta})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
