from fastapi import FastAPI
from app.config import get_settings
from app.database import create_tables
from app.models import user

settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    version='1.0.0',
    debug=settings.app_debug,
    docs_url='/docs' if not settings.is_production else None,
    redoc_url='/redoc' if not settings.is_production else None
)