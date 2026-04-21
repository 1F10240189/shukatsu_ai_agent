# backend/fastapi_app/core/database.py
# DB接続設定。エンジン・セッション・Baseクラスを定義
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# .envからDB接続先を取得
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./shukatsu.db")

# DBエンジン(DBへの接続設定)作成、
# connect_args はSQLite使用時のみ必要な設定
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# DBセッション（操作のための接続）を作成
# セッションはDBへの操作窓口（1リクエスト1セッション）
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 全モデルの基底クラス（全テーブルはこれを継承する）
Base = declarative_base()

# エンドポイントにDBを渡す関数
def get_db():
    """
    DBセッションを提供する関数
    APIのエンドポイントで使用する
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()