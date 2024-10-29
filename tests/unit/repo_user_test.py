import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.models.users import User
from app.db.repository.user import UserRepository


# Create an SQLite in-memory database
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
@pytest.fixture(scope="function")
def db_session():
    # Create the database tables
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.mark.asyncio
async def test_get_user(db_session):
    # Arrange
    user_repo = UserRepository(db=db_session)
    test_user = User(
        first_name="Test",
        last_name="User",
        username="testuser",
        email="testuser@example.com")
    user_repo.create(test_user)

    # Act
    result = await user_repo.get_user(username="testuser")

    # Assert
    assert result is not None
    assert result.username == "testuser"
    assert result.email == "testuser@example.com"