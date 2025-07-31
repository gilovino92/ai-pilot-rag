from fastapi import APIRouter

from app.core.config import settings
from app.api.routes import knowledge, utils, tenant

api_router = APIRouter()

api_router.include_router(knowledge.router)
api_router.include_router(utils.router)
api_router.include_router(tenant.router)