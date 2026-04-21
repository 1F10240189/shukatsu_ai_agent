# backend/fastapi_app/api/v1/router.py
# エンドポイントをまとめてURLプレフィックスを付ける
from fastapi import APIRouter
from api.v1.endpoints import auth

router = APIRouter()

# /api/v1/auth/register
# /api/v1/auth/login
router.include_router(auth.router, prefix="/auth", tags=["認証"])