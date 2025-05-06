from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn

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
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

    # return """
    # <html>
    #     <head style="text-align: center; background-color: #f0f0f0; padding: 20px;">
    #         <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    #         <title>FastAPI Server</title>
    #     </head>
    #     <body style="text-align: center; background-color: #f0f0f0; padding: 20px;">
    #         <h1 style="color: #333;">FastAPI Server</h1>
    #         <p style="color: #555;">This is a simple FastAPI application serving a React frontend.</p>
    #         <p style="color: #555;">You can access the frontend at <a href="http://localhost:4200" style="color: #007bff;">http://localhost:4200</a></p>
    #     </body>
    # </html>
    # """

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9999)
