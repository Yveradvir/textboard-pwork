from datetime import timedelta
from pydantic import BaseModel

class CabaleSettings(BaseModel):
    max_age: float = timedelta(minutes=30).seconds
    trigger_at: float = timedelta(minutes=25).seconds
    key: str