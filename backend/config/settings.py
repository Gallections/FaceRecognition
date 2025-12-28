"""
Application configuration settings
"""
import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra='ignore'
    )
    
    # Application Settings
    APP_NAME: str = "Face Recognition Attendance System"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = False
    
    # API Settings
    API_PREFIX: str = "/api/v1"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:5174"]
    
    # Database Settings
    DB_NAME: str = "facialRecognition"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = ""
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    
    # File Upload Settings
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_TYPES: List[str] = ["image/jpeg", "image/png", "image/jpg"]
    
    # Face Recognition Settings
    FACE_DETECTION_MODEL: str = "hog"  # or "cnn" for better accuracy but slower
    FACE_RECOGNITION_TOLERANCE: float = 0.6


# Create global settings instance
settings = Settings()
