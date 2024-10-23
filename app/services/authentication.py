from fastapi.params import Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql.annotation import Annotated

from app.db.session import get_db
from app.models.users import User


class Authentication:
    def __init__(self, db: Session):
        self.db = db

    def get_authentication(self):
        data = self.db.query(User).all()
        return data