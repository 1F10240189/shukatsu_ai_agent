# backend/fastapi_app/models/user.py
# usersテーブルの定義
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # リレーション（Userに紐づくデータを取得できるようにする）
    companies = relationship("Company", back_populates="user")
    offer_sites = relationship("UserOfferSite", back_populates="user")