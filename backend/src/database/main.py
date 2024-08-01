from uuid import uuid4
from base64 import b64decode, b64encode
from datetime import datetime, timezone

from sqlalchemy import UUID, Column

from sqlalchemy.types import Uuid, String, Integer, Boolean, LargeBinary, DateTime, Text, Date
from sqlalchemy.orm import declarative_base


class InitialMixin(object):
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid4)

    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self):
        """Converts the SQLAlchemy model instance to a dictionary."""
        data = {}

        for col in self.__table__.columns:
            if isinstance(col.type, LargeBinary):
                binary_data = getattr(self, col.name)
                if binary_data:
                    data[col.name] = b64encode(
                        getattr(self, col.name)
                    ).decode()
                else:
                    data[col.name] = None
            elif isinstance(col.type, (Date, DateTime)):
                date_data = getattr(self, col.name).isoformat()
                data[col.name] = date_data
            elif isinstance(col.type, (Uuid, UUID)):
                data[col.name] = str(getattr(self, col.name))
            else:
                data[col.name] = getattr(self, col.name)

        return data


Base = declarative_base()