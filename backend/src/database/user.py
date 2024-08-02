from src.database import db
from src.database.main import *

class UserTable(db.base, db.mixin):
    __tablename__ = 'users'
    
    username = Column(String(30), nullable=False, unique=True)
    password = Column(String, nullable=False)
    
    iv = Column(String, nullable=False, unique=True)