# backend/fastapi_app/main.py
# アプリの入口。サーバー起動・ルーター登録・DB初期化
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import engine, Base
from api.v1.router import router

import models.user
import models.offer
import models.company

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="就活AI分析アプリ",
    description="オファーサイトの企業をAIで分析するAPI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターを登録
app.include_router(router, prefix="/api/v1")


@app.get("/")
def health_check():
    return {"status": "ok", "message": "就活AI分析アプリ起動中"}