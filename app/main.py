import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import CORS_ORIGINS
from app.routes.forge import router as forge_router
import uvicorn

app = FastAPI(title="AudioForge")

# Parse CORS origins (comma-separated string)
origins = [o.strip() for o in CORS_ORIGINS.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)

# Register routes
app.include_router(forge_router, prefix="/forge", tags=["Forge"])

if __name__ == "__main__":
    # IMPORTANT: use import string so reload works
    uvicorn.run(
        "app.main:app",    # <-- correct import string
        host="127.0.0.5",
        port=8080,
        reload=True
    )
