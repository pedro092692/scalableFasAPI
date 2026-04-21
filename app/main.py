from fastapi import FastAPI
from app.config import get_settings
from app.api.router import api_router
from app.database import create_tables
from app.core.middleware import RequestLoggingMiddleware
from app.core.errors import validation_exception_handler
from fastapi.exceptions import RequestValidationError
from app.core.logging import setup_logging
# mongoDB
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.user_mongo import UserDocument
from app.database_mongo import get_mongo_client
from contextlib import asynccontextmanager


settings = get_settings()
setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Arranca ──────────────────────────────────────
    client = AsyncIOMotorClient(settings.mongodb_url)
    await init_beanie(
        database=client[settings.mongodb_db_name],
        document_models=[UserDocument]  # agrega todos tus modelos aquí
    )
    print("✅ MongoDB conectado y Beanie inicializado")

    yield  # la app corre aquí

    # ── Apaga ─────────────────────────────────────────
    client.close()
    print("MongoDB desconectado")

app = FastAPI(
    title=settings.app_name,
    version='1.0.0',
    debug=settings.app_debug,
    docs_url='/docs' if not settings.is_production else None,
    redoc_url='/redoc' if not settings.is_production else None,
    lifespan=lifespan
)


app.add_middleware(RequestLoggingMiddleware)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.include_router(api_router, prefix='/api/v1')

if not settings.is_production:
    create_tables()


@app.get('/health', tags=['Health'])
def health_check():
    return {'status': 'ok', 'env': settings.app_env}