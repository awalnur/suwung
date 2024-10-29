import re
import uuid
from datetime import datetime

from sqlalchemy import Column, UUID, DateTime
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import declarative_base

class AutoNameMeta(DeclarativeMeta):
    def __init__(cls, name, bases, d):
        if '__tablename__' not in d:
            pattern = re.compile(r'(?<!^)(?=[A-Z])')
            table_name = pattern.sub('_', cls.__name__).lower()
            setattr(cls, '__tablename__', f'{table_name}s')
        super().__init__(name, bases, d)

class CustomBase:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"

Base = declarative_base(metaclass=AutoNameMeta)
