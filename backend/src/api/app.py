import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from database.db import create_tables
from routes import auth_routes, patient_routes, user_routes, graph_routes
from fastapi.staticfiles import StaticFiles

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
    secret_key="by$3n%5i*!j!e**%czytj+or22eyw-r*td$9yl-9yw077_&cb",
    session_cookie="session",
    max_age=14 * 24 * 60 * 60,
    same_site="lax",
)


# Ruta absoluta al directorio 'src/static'
base_dir = os.path.dirname(os.path.abspath(__file__))  # src/api/
static_dir = os.path.abspath(os.path.join(base_dir, "..", "static"))

# Crear el directorio si no existe
os.makedirs(static_dir, exist_ok=True)

# Montar los archivos estáticos
app.mount("/static", StaticFiles(directory=static_dir), name="static")


api_prefix = "/api/v1"

app.include_router(auth_routes.router, prefix=api_prefix)
app.include_router(patient_routes.router, prefix=api_prefix)
app.include_router(user_routes.router, prefix=api_prefix)
app.include_router(graph_routes.router, prefix=api_prefix)

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
