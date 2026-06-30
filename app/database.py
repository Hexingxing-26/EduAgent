from sqlalchemy import create_engine, Column, String, Text, DateTime, Integer, Index, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./edu_agent.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class EduUser(Base):
    __tablename__ = "edu_user"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    nickname = Column(String(50))
    major = Column(String(50))
    create_time = Column(DateTime, default=datetime.now)


class EduChat(Base):
    __tablename__ = "edu_chat"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer)
    session_id = Column(String(100))
    content = Column(Text)
    role = Column(String(20))
    create_time = Column(DateTime, default=datetime.now)


class EduProfile(Base):
    __tablename__ = "edu_profile"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, unique=True)
    weak_points = Column(Text)
    learning_json = Column(Text)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class EduResource(Base):
    __tablename__ = "edu_resource"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer)
    resource_type = Column(String(30))
    content = Column(Text)
    progress = Column(Integer, default=0)
    create_time = Column(DateTime, default=datetime.now)


class LearningRecord(Base):
    __tablename__ = "learning_records"
    id = Column(String(50), primary_key=True)
    user_id = Column(String(50), nullable=False, index=True)
    course = Column(String(100))
    chapter = Column(String(200))
    score = Column(Float)
    correct_rate = Column(Float)
    problems_done = Column(Integer)
    duration_minutes = Column(Integer)
    date = Column(Date)
    time_slot = Column(String(50))


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()