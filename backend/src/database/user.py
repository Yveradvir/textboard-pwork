from src.database import db
from src.database.main import *

from sqlalchemy.orm import relationship

class UserTable(db.base, db.mixin):
    __tablename__ = 'users'
    
    username = Column(String(30), nullable=False, unique=True)
    password = Column(String, nullable=False)
    
    iv = Column(String, nullable=False, unique=True)
    memberships = relationship("MembershipTable", back_populates="users", cascade="all, delete-orphan")
