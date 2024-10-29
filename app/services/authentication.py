from sqlalchemy.orm import Session

from app.db.models.users import User
from app.db.repository.user import UserRepository


class Authentication:
    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository()
    def get_authentication(self, username: str, password: str):
        user_data = self.repository.find_by_username(username=username)
        return user_data