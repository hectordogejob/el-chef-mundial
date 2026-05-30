from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

CONNECTION_STRING = (
    "mssql+pyodbc://@(localdb)\\MSSQLLocalDB/ElChefMundial"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)

engine = create_engine(CONNECTION_STRING)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
