from fastapi import FastAPI
from app.routes.forge import router as forge_router
import uvicorn

app = FastAPI(title="AudioForge")

# Register routes
app.include_router(forge_router, prefix="/forge", tags=["Forge"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.5", port=8080, reload=True)
