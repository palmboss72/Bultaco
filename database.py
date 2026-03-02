import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Render provides the database URL in the environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./local_dev.db")

# SQLAlchemy requires 'postgresql://' instead of Render's default 'postgres://'
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()