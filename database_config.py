from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123@localhost/ozon"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:loT0ok5kSawf4S53o9JL@containers-us-west-43.railway.app:5704/railway"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()
