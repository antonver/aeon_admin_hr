from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import uvicorn
from dotenv import load_dotenv
import os

# Импорты для работы с Render - используем относительные импорты
from app.database import engine, Base
from app.routers import candidates, metrics, user, telegram_auth, admins, external_api
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

# CORS middleware - расширенные настройки для всех источников
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000", 
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:8001",
        "http://127.0.0.1:8001",
        "https://localhost:3000",
        "https://127.0.0.1:3000",
        "https://localhost:3001", 
        "https://127.0.0.1:3001",
        "https://localhost:8000",
        "https://127.0.0.1:8000",
        "https://localhost:8001",
        "https://127.0.0.1:8001",
        "http://0.0.0.0:3000",
        "http://0.0.0.0:3001",
        "http://0.0.0.0:8000",
        "http://0.0.0.0:8001",
        "https://0.0.0.0:3000",
        "https://0.0.0.0:3001", 
        "https://0.0.0.0:8000",
        "https://0.0.0.0:8001",
        "*"  # Разрешаем все источники
    ],
    allow_credentials=True,
    allow_methods=[
        "GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"
    ],
    allow_headers=[
        "Accept",
        "Accept-Language", 
        "Content-Language",
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "Origin",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers",
        "Cache-Control",
        "Pragma",
        "Expires",
        "X-CSRF-Token",
        "X-API-Key",
        "X-Client-Version",
        "User-Agent",
        "Referer",
        "DNT",
        "Accept-Encoding",
        "Accept-Charset",
        "Connection",
        "Host",
        "Upgrade-Insecure-Requests",
        "Sec-Fetch-Dest",
        "Sec-Fetch-Mode", 
        "Sec-Fetch-Site",
        "Sec-Fetch-User",
        "*"  # Разрешаем все заголовки
    ],
    expose_headers=[
        "Content-Length",
        "Content-Range",
        "X-Total-Count",
        "X-Page-Count",
        "X-Current-Page",
        "X-Next-Page",
        "X-Prev-Page",
        "X-Total-Pages",
        "X-Has-Next",
        "X-Has-Prev",
        "X-Request-ID",
        "X-Response-Time",
        "X-Rate-Limit-Limit",
        "X-Rate-Limit-Remaining",
        "X-Rate-Limit-Reset",
        "X-Powered-By",
        "Server",
        "Date",
        "ETag",
        "Last-Modified",
        "Cache-Control",
        "Pragma",
        "Expires",
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Methods",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Credentials",
        "Access-Control-Max-Age",
        "Access-Control-Expose-Headers"
    ],
    max_age=86400,  # 24 часа кэширования preflight запросов
)

# Подключаем роутеры
app.include_router(candidates.router, prefix="/api/candidates", tags=["candidates"])

app.include_router(metrics.router, prefix="/api/metrics", tags=["metrics"])
app.include_router(user.router, prefix="/api/user", tags=["user"])
app.include_router(telegram_auth.router, prefix="/api/telegram", tags=["telegram"])
app.include_router(admins.router, prefix="/api", tags=["admins"])
app.include_router(external_api.router, prefix="/api/external", tags=["external"])

# Подключаем статические файлы с отключением кэширования
from fastapi.responses import Response
from fastapi import Request

@app.middleware("http")
async def add_no_cache_headers(request: Request, call_next):
    response = await call_next(request)
    
    # Отключаем кэширование для статических файлов
    if request.url.path.startswith("/static/"):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    
    return response

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    try:
        return FileResponse("static/index.html")
    except FileNotFoundError:
        return {"message": "HR Admin Panel Backend API", "frontend": "not built"}

@app.get("/manifest.json")
async def manifest():
    try:
        return FileResponse("static/manifest.json")
    except FileNotFoundError:
        return {"message": "Manifest not found"}

@app.get("/test-telegram")
async def test_telegram():
    try:
        return FileResponse("static/test-telegram.html")
    except FileNotFoundError:
        return {"message": "Test page not found"}

@app.get("/test-external-api")
async def test_external_api():
    try:
        return FileResponse("static/test-external-api.html")
    except FileNotFoundError:
        return {"message": "Test page not found"}

@app.get("/debug")
async def debug():
    try:
        return FileResponse("static/debug.html")
    except FileNotFoundError:
        return {"message": "Debug page not found"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/health")
async def api_health_check():
    return {"status": "healthy"}

@app.get("/api/")
async def api_root():
    return {"message": "HR Admin Panel API", "version": "1.0.0"}

@app.options("/{full_path:path}")
async def options_handler(full_path: str):
    """Обработчик OPTIONS запросов для CORS preflight"""
    return {"message": "OK"}

# Catch-all route для SPA
@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    # Если это API запрос, возвращаем 404
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API endpoint not found")
    
    # Для всех остальных путей возвращаем index.html
    try:
        return FileResponse("static/index.html")
    except FileNotFoundError:
        return {"message": "Frontend not built", "api_docs": "/docs"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 