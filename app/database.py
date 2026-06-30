from sqlalchemy import create_engine, Column, String, Text, JSON, DateTime, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ai_agent.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    user_id = Column(String(50), primary_key=True, index=True)
    knowledge_base = Column(String(50), nullable=False)
    cognitive_style = Column(String(50), nullable=False)
    weak_points = Column(Text, nullable=True)
    interest = Column(String(100), nullable=True)
    learning_pace = Column(String(20), nullable=False)
    emotional_state = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class LearningRecord(Base):
    __tablename__ = "learning_records"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(50), nullable=False, index=True)
    topic = Column(String(200), nullable=False)
    profile = Column(JSON, nullable=True)
    generated_resource = Column(Text, nullable=True)
    learning_path = Column(JSON, nullable=True)
    is_approved = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)


class KnowledgeBase(Base):
    __tablename__ = "knowledge_base"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    content = Column(Text, nullable=False)
    keywords = Column(String(200), nullable=True)
    category = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.now)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()