from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import uvicorn
from dotenv import load_dotenv
import os

from app.database import engine, Base
from app.routers import candidates, notifications, metrics, user, telegram_auth
from app.services.telegram_service import TelegramService
from app.services.notion_service import NotionService

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown

app = FastAPI(
    title="HR Admin Panel",
    description="HR-админ панель для управления кандидатами",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(candidates.router, prefix="/api/candidates", tags=["candidates"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["notifications"])
app.include_router(metrics.router, prefix="/api/metrics", tags=["metrics"])
app.include_router(user.router, prefix="/api/user", tags=["user"])
app.include_router(telegram_auth.router, prefix="/api/telegram", tags=["telegram"])

# Подключаем статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.get("/manifest.json")
async def manifest():
    return FileResponse("static/manifest.json")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/health")
async def api_health_check():
    return {"status": "healthy"}

@app.get("/api/")
async def api_root():
    return {"message": "HR Admin Panel API", "version": "1.0.0"}

# Catch-all route для SPA
@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    # Если это API запрос, пропускаем
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API endpoint not found")
    
    # Для всех остальных путей возвращаем index.html
    return FileResponse("static/index.html")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 