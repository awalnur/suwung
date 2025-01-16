from datetime import timedelta, datetime

from app.core.config import settings
from app.db.models.users import User, RefreshToken
from app.db.session import get_db


class UserRepository:
    def __init__(self, db=next(get_db())):
        self.db = db

    def create(self, user):
        self.db.add(user)
        self.db.commit()
        return user


    async def get_refresh_token(self, user_id):
        return self.db.query(RefreshToken).filter(RefreshToken.user_id == user_id).first()


    async def set_refresh_token(self, user, refresh_token):

        expires =timedelta(minutes=settings.REFRESH_TOKEN_EXPIRATION)
        try:
            _check = self.db.query(RefreshToken).filter(RefreshToken.user_id == user.id).first()
            if _check is not None:
                _check.token = refresh_token
                _check.expires = expires
                self.db.commit()
            else:
                refresh_token= RefreshToken(user_id=user.id, token=refresh_token, expires=expires)
                self.db.add(refresh_token)
                self.db.commit()

            return refresh_token
        except Exception as e:
            print(e)
            return None
    async def get_user(self, **kwargs):
        filter = User.__dict__
        for key in kwargs:
            if key not in filter:
                raise KeyError(f"Key {key} not found in User")

        return self.db.query(User).filter_by(**kwargs).first()

    def find_by_username(self, username):
        return self.db.query(User).filter(User.username == username).one()

    def get_find_by(self, username, *args):
        return self.db.query()

    def find_by_id(self, user_id):
        return self.db.query(User).filter(User.id == user_id).first()

    def find_by_email(self, email):
        return self.db.query(User).filter(User.email == email).first()

    def find_all(self):
        return self.db.query(User).all()

    def update(self, user):
        self.db.commit()
        return user

    def delete(self, user):
        self.db.delete(user)
        self.db.commit()
        return user

    def __repr__(self):
        return f"<UserRepository(db={self.db})>"