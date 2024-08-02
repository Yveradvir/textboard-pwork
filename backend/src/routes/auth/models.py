from pydantic import BaseModel

class AuthBodyModel(BaseModel):
    username: str
    password: str