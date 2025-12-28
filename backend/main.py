"""
Face Recognition Attendance System - FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.config import settings
from backend.api.routes import persons, face_recognition, attendance
from database.db import DatabaseManager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle - database connections and cleanup"""
    DatabaseManager.initialize_pool()
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} - Database: {settings.DB_NAME}")
    yield
    DatabaseManager.close_all_connections()
    print("👋 Shutdown complete")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Face Recognition Attendance System API",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Register API routes
app.include_router(persons.router, prefix=settings.API_PREFIX)
app.include_router(face_recognition.router, prefix=settings.API_PREFIX)
app.include_router(attendance.router, prefix=settings.API_PREFIX)


@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)