from sqlalchemy import Column, String, ForeignKey, UUID, Interval, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.db.base import Base, CustomBase


class User(Base, CustomBase):
    username = Column(String, unique=True, index=True)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = relationship("Password", back_populates="user")
    refresh_token = relationship("RefreshToken", back_populates="user")
class Password(Base):
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
    password_hash = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    user = relationship("User", back_populates="password")

class RefreshToken(Base, CustomBase):
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
    token = Column(String, nullable=False)
    expires = Column(Interval, nullable=False)
    revoked = Column(Boolean, default=False)
    revoked_at = Column(DateTime, nullable=True)
    user = relationship("User", back_populates="refresh_token")
