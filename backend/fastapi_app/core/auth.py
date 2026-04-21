# backend/fastapi_app/core/auth.py
# 認証ロジック。パスワード暗号化・JWT発行・検証
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# パスワードの暗号化設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """パスワードを暗号化する"""
    # "password123" → "$2b$12$xxxxx..." という形に変換
    # 元のパスワードには戻せない（一方向）
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """入力されたパスワードとDB内の暗号化パスワードを照合する"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """JWTトークンを発行する"""
    # SECRET_KEYで署名するので改ざんできない
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    """JWTトークンを検証して中身を取り出す"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None