from src.database import db
from src.database.main import *

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class TexboardTable(db.base, db.mixin):
    __tablename__ = 'texboards'
    
    name = Column(String(30), nullable=False, unique=True)
    password = Column(String, nullable=True)
    
    owner_id = Column(String(30), ForeignKey('users.id'))

    memberships = relationship("MembershipTable", back_populates="textboards", cascade="all, delete-orphan")