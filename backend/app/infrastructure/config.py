"""
Application configuration settings
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Server settings
    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = True
    
    # OpenAI API settings
    openai_api_key: str
    openai_model: str = "gpt-4"
    openai_max_tokens: int = 2000
    openai_temperature: float = 0.7
    
    # Database settings
    database_url: str = "sqlite:///./sheikh.db"
    
    # Security settings
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # File system settings
    upload_directory: str = "./uploads"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    
    # Shell execution settings
    shell_timeout: int = 30  # seconds
    allowed_commands: list[str] = [
        "ls", "cat", "grep", "find", "wc", "head", "tail", "sort", "uniq"
    ]
    
    # Browser automation settings
    browser_headless: bool = True
    browser_timeout: int = 30  # seconds
    browser_user_data_dir: str = "./browser/user_data"
    
    # Redis settings (for caching and sessions)
    redis_url: str = "redis://localhost:6379/0"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()