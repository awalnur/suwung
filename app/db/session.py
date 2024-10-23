from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine  = create_engine('sqlite:///.db.sqlite3')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
