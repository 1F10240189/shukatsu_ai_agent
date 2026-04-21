# backend/fastapi_app/models/offer.py
# offer_site_masters・user_offer_sitesテーブルの定義
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base


class OfferSiteMaster(Base):
    """オファーサイトのマスターデータ（開発者が事前定義）"""
    __tablename__ = "offer_site_masters"

    id = Column(Integer, primary_key=True, index=True)
    site_name = Column(String, nullable=False)
    sender_email = Column(String, nullable=False)
    regex_pattern = Column(Text)
    ai_prompt = Column(Text)

    user_sites = relationship("UserOfferSite", back_populates="site_master")


class UserOfferSite(Base):
    """ユーザーが登録したオファーサイト"""
    __tablename__ = "user_offer_sites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False) # usersテーブルのidと紐づける
    site_master_id = Column(Integer, ForeignKey("offer_site_masters.id"), nullable=False)
    registered_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="offer_sites")
    site_master = relationship("OfferSiteMaster", back_populates="user_sites")