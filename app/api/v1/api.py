# app/api/api_v1/api.py
from fastapi import APIRouter

from app.api.v1.endpoints import admin,session, common, settings

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(admin.router, prefix='/admin',tags=["Admin"])
api_router.include_router(common.router, prefix='/common',tags=["Common"])
api_router.include_router(settings.router, prefix='/settings',tags=["Settings"])


api_router.include_router(session.router, tags=["session"])
