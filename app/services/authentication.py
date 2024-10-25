from sqlalchemy.orm import Session

from app.db.models.users import User


class Authentication:
    def __init__(self, db: Session):
        self.db = db

    def get_authentication(self):
        data = self.db.query(User).all()
        return data