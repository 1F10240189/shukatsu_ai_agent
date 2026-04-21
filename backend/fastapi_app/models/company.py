# backend/fastapi_app/models/company.py
# companies・company_analysesテーブルの定義
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base


class Company(Base):
    """企業情報"""
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    source_site_id = Column(Integer, ForeignKey("offer_site_masters.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="companies")
    analysis = relationship("CompanyAnalysis", back_populates="company", uselist=False)


class CompanyAnalysis(Base):
    """AI分析結果"""
    __tablename__ = "company_analyses"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    summary = Column(Text)
    salary = Column(Integer, nullable=True)
    overtime = Column(Integer, nullable=True)
    black_score = Column(Integer, nullable=True)
    raw_response = Column(Text)
    analyzed_at = Column(DateTime(timezone=True), server_default=func.now())

    company = relationship("Company", back_populates="analysis")