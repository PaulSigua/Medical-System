import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from database.db import create_tables
from routes.patients import patient_routes
from routes import auth_routes, user_routes
from routes.upload_nifti import upload_file
from routes.ai import detection_routes
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

import os
for var in ["nnUNetv2_results", "nnUNetv2_raw", "nnUNetv2_preprocessed"]:
    if not os.getenv(var):
        raise RuntimeError(f"Variable {var} no cargada desde .env")


# Cargar las variables de entorno desde el archivo .env
load_dotenv()
# Obtener la ruta del archivo .env
env_path = os.path.join(os.path.dirname(__file__), '..', 'services', '.env')
load_dotenv(dotenv_path=os.path.abspath(env_path))
# print("nnUNetv2_results =", os.getenv("nnUNetv2_results"))

SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI(
    title="FastAPI Server",
    description="Medical System Aplication.",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "root",
            "description": "Root endpoint",
        },
    ],
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS middleware to allow requests from the frontend

origins = [
    "http://localhost:4200",
    # "*"
]

# 1) CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2) Session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    session_cookie="session",
    max_age=14 * 24 * 60 * 60,
    same_site="lax",
)


# Ruta absoluta al directorio 'src/static'
base_dir = os.path.dirname(os.path.abspath(__file__))  # src/api/
uploads_dir = os.path.abspath(os.path.join(base_dir, "..", "uploads"))
processed_files_dir = os.path.abspath(os.path.join(base_dir, "..", "processed_files"))
static_dir = os.path.abspath(os.path.join(base_dir, "..", "static"))

# Crear el directorio si no existe
os.makedirs(uploads_dir, exist_ok=True)
os.makedirs(processed_files_dir, exist_ok=True)
os.makedirs(static_dir, exist_ok=True)

# Montar los archivos estáticos
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")
app.mount("/processed_files", StaticFiles(directory=processed_files_dir), name="processed_files")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

api_prefix = "/api/v1"

app.include_router(auth_routes.router, prefix=api_prefix)
app.include_router(patient_routes.router, prefix=api_prefix)
app.include_router(user_routes.router, prefix=api_prefix)
app.include_router(upload_file.router, prefix=api_prefix)
# app.include_router(graph_routes.router, prefix=api_prefix)
app.include_router(detection_routes.router, prefix=api_prefix)

@app.get("/", description="Root endpoint")
async def read_root():
    try:
        info = [
            {
                "status": "success",
                "name": "FastAPI Server",
                "description": "Medical System Aplication.",
                "version": "1.0.0",
            },
            {
                "frontend": "http://localhost:4200",
                "backend": "http://localhost:9999",
            },
            {
                "docs": "http://localhost:9999/docs",
                "redoc": "http://localhost:9999/redoc",
                "openapi": "http://localhost:9999/openapi.json",
            },
            {
                "author": "Paúl Sigua, Jeison Pañora y David Alvarado"
            }
        ]
        return info
    except HTTPException as e:
        info = [
            {
                "status": f"error: {e.detail}, status_code={e.status_code}"
            }
        ]
        return info

# create_tables()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9999)