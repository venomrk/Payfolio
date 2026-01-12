from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Payfolio API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str
    
    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str
    
    # JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Stripe
    STRIPE_SECRET_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    
    # Razorpay
    RAZORPAY_KEY_ID: str = ""
    RAZORPAY_KEY_SECRET: str = ""
    
    # AI
    GEMINI_API_KEY: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
