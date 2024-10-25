
import uuid
from datetime import datetime

from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import User, Password

def seed_data(db: Session = Depends(get_db)):
    # Create a new session

    # Create tables
    # Base.metadata.create_all(engine)
    # Add initial data
    user1 = User(
        id=uuid.uuid4(),
        username='johndoe',
        first_name='John',
        last_name='Doe',
        email='johndoe@example.com',
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


    password1 = Password(
        user_id=user1.id,
        password_hash='hashed_password_1',
        salt='salt_1'
    )

    # user1.password = password1

    # user1.password = password1

    db.add(user1)
    db.commit()

    # Close the session
    db.close()

if __name__ == "__main__":
    db = next(get_db())
    seed_data(db)