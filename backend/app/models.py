"""
FDA Warning Letter System - Database Models
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, Date, DateTime, ForeignKey, Table, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:////root/data/fda_warning.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class WarningLetter(Base):
    __tablename__ = 'warning_letters'

    id = Column(Integer, primary_key=True)
    fda_id = Column(String(50), unique=True)
    slug = Column(String(255))
    posted_date = Column(Date)
    issue_date = Column(Date)
    company_name = Column(String(500))
    issuing_office = Column(String(255))
    subject = Column(Text)
    fei_number = Column(String(50))
    country = Column(String(100))        # 国家
    region = Column(String(100))        # 省份/地域
    full_text = Column(Text)
    full_text_clean = Column(Text)
    url = Column(String(500))
    closeout_date = Column(Date, nullable=True)
    response_date = Column(Date, nullable=True)
    closeout_pdf_url = Column(String(500), nullable=True)
    status = Column(String(50))          # Open / Closed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    violations = relationship('Violation', back_populates='letter')
    ai_analysis = relationship('AIAnalysis', back_populates='letter', uselist=False)
    f483_observations = relationship('F483Observation', back_populates='letter')
    cfr_citations = relationship('CFRCitation', back_populates='letter')


class Violation(Base):
    __tablename__ = 'violations'

    id = Column(Integer, primary_key=True)
    letter_id = Column(Integer, ForeignKey('warning_letters.id'))
    # CGMP六大系统: Quality System, Production System, Facility and Equipment,
    # Materials System, Personnel, Production and Process Controls
    system = Column(String(100))
    description = Column(Text)
    cfr_code = Column(String(50))
    letter = relationship('WarningLetter', back_populates='violations')


class AIAnalysis(Base):
    __tablename__ = 'ai_analysis'

    id = Column(Integer, primary_key=True)
    letter_id = Column('warning_letter_id', Integer, ForeignKey('warning_letters.id'), unique=True)
    translation_zh = Column(Text)        # 中文翻译
    summary_zh = Column(Text)            # 中文摘要
    violation_type = Column(String(100)) # CGMP违规分类
    key_findings = Column(JSON)          # 关键发现
    risk_level = Column(String(20))      # High / Medium / Low
    model_used = Column(String(128))    # 模型名称
    analyzed_at = Column(DateTime, default=datetime.utcnow)
    letter = relationship('WarningLetter', back_populates='ai_analysis')


class F483Observation(Base):
    __tablename__ = 'f483_observations'

    id = Column(Integer, primary_key=True)
    letter_id = Column(Integer, ForeignKey('warning_letters.id'))
    observation_number = Column(String(10))  # e.g. "Obs. 1"
    description = Column(Text)
    cfr_reference = Column(String(100))
    letter = relationship('WarningLetter', back_populates='f483_observations')


class CFRCitation(Base):
    __tablename__ = 'cfr_citations'

    id = Column(Integer, primary_key=True)
    letter_id = Column(Integer, ForeignKey('warning_letters.id'))
    cfr_section = Column(String(50))
    description = Column(Text)
    letter = relationship('WarningLetter', back_populates='cfr_citations')


class PushSubscription(Base):
    __tablename__ = 'push_subscriptions'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(100))       # Telegram user_id 或 email
    platform = Column(String(20))        # telegram / email
    keywords_filter = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Integer, default=1)
