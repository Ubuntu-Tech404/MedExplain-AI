import os
from typing import Optional
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    # App
    app_name: str = "Mediclinic AI Dashboard"
    app_version: str = "2.0.0"
    debug: bool = False
    environment: str = "development"
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_prefix: str = "/api"
    cors_origins: list = ["http://localhost:3000", "http://localhost:5173"]
    
    # Hugging Face
    hf_token: Optional[str] = None
    hf_model_name: str = "meta-llama/Llama-3.2-11B"
    hf_cache_dir: str = "./cache"
    
    # Supabase
    supabase_url: Optional[str] = None
    supabase_anon_key: Optional[str] = None
    supabase_service_role_key: Optional[str] = None
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # File Upload
    max_upload_size_mb: int = 100
    allowed_extensions: list = [".pdf", ".docx", ".txt", ".jpg", ".png", ".jpeg"]
    upload_dir: str = "./static/uploads"
    
    # Demo Mode
    demo_mode: bool = True
    use_mock_data: bool = True
    
    # Model Settings
    model_max_tokens: int = 512
    model_temperature: float = 0.7
    model_top_p: float = 0.95
    
    # Redis (optional)
    redis_url: Optional[str] = None
    
    # Email (optional)
    smtp_server: Optional[str] = None
    smtp_port: Optional[int] = None
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

def get_settings() -> Settings:
    """Get application settings"""
    return Settings()

# Global settings instance
settings = get_settings()