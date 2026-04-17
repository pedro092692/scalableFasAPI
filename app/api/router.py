from fastapi import APIRouter
from app.api.v1 import users, item

api_router = APIRouter()

items_module = item.Item().router

api_router.include_router(users.router)
api_router.include_router(items_module)