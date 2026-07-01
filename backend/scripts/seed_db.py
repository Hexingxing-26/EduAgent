#!/usr/bin/env python3
"""Seed the database with initial admin user and sample data."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from database.connect import SessionLocal, engine, Base
from database.models import EduUser
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed():
    # Create tables if not exist (for SQLite dev first run)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Import after path setup to avoid circular imports
        from database.crud import get_user_by_username

        # Create admin user if not exists
        if not get_user_by_username(db, "admin"):
            admin = EduUser(
                username="admin",
                password=pwd_context.hash("admin123"),
                nickname="管理员",
                major="系统管理"
            )
            db.add(admin)
            print("Created admin user: admin/admin123")

        # Create demo student user if not exists
        if not get_user_by_username(db, "student1"):
            student = EduUser(
                username="student1",
                password=pwd_context.hash("123456"),
                nickname="学生一",
                major="计算机科学"
            )
            db.add(student)
            print("Created student user: student1/123456")

        db.commit()
        print("Database seeded successfully!")
    except Exception as e:
        db.rollback()
        print(f"Seed error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed()
