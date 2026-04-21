from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.config import get_settings

settings = get_settings()

# global client - its creates once when app starts
mongo_client: AsyncIOMotorClient = None


def get_mongo_client() -> AsyncIOMotorClient:
    return AsyncIOMotorClient(settings.mongodb_url)


def get_mongo_db() -> AsyncIOMotorDatabase:
    client = get_mongo_client()
    return client[settings.mongodb_db_name]