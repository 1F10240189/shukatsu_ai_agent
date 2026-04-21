# backend/fastapi_app/schemas/user.py
# ユーザー登録・ログイン・レスポンスの型定義
"""Model  → DBのテーブル定義（SQLAlchemy）
   Schema → APIの入出力の型定義（Pydantic）"""
from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    """ユーザー登録時の入力データ"""
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """ログイン時の入力データ"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """APIがユーザー情報を返すときの形式（パスワードは含めない）"""
    id: int
    email: str

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """ログイン成功時に返すトークン"""
    access_token: str
    token_type: str = "bearer"