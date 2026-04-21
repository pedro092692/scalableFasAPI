from fastapi import APIRouter
from app.api.v1 import users, item, users_mongo

api_router = APIRouter()

items_module = item.Item().router

api_router.include_router(users.router)
api_router.include_router(users_mongo.router)
api_router.include_router(items_module)
