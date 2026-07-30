import os

class Settings:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRY_MINUTES = int(os.environ.get("JWT_EXPIRY_MINUTES", "30"))
    DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///dev.db")
    REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    SMTP_HOST = os.environ.get("SMTP_HOST", "localhost")
    SMTP_PORT = int(os.environ.get("SMTP_PORT", "25"))
    PAYMENT_GATEWAY_URL = os.environ.get("PAYMENT_GATEWAY_URL", "https://api.payments.test/v1")
    PAYMENT_API_KEY = os.environ.get("PAYMENT_API_KEY", "test-key")
    CACHE_TTL = int(os.environ.get("CACHE_TTL", "300"))
    RATE_LIMIT_PER_MINUTE = int(os.environ.get("RATE_LIMIT_PER_MINUTE", "1000"))
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

settings = Settings()
