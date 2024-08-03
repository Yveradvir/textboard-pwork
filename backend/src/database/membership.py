from src.database import db
from src.database.main import *

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

        
class MembershipTable(db.base, db.mixin):
    __tablename__ = 'memberships'
    
    user_id = Column(String(30), ForeignKey('users.id'), nullable=False, unique=True)
    textboard_id = Column(String, ForeignKey('textboards.id'), nullable=False)
    mtype = Column(Integer, default=0)
        # 0 - user
        # 1 - admin
        # 2 - banned 

    user = relationship("UserTable", back_populates="memberships", cascade="all, delete-orphan")
    textboard = relationship("TextboardTable", back_populates="memberships", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<MembershipTable(user_id={self.user_id}, textboard_id={self.textboard_id}, mtype={self.mtype})>"
