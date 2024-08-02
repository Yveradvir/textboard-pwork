from typing import Union
from uuid import UUID
from os import urandom
from base64 import b64decode, b64encode

from fastapi import Depends, HTTPException
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.security import APIKeyCookie

from src.database import db
from src.database.user import UserTable
from src.core.security.cabale_manager import cabale

from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

api_cabale = APIKeyCookie(
    name="cabale",
    scheme_name="cabale_cookie",
    description="The cookie for Cabale authentication"
)

class CabaleAuthManager:
    def __init__(self) -> None:
        """
        Initialize the CabaleAuthManager class.
        """
        pass
    
    def generate_iv(self) -> str:
        """Generate a random initialization vector (IV) for encryption."""
        return b64encode(urandom(16)).decode()
        
    async def get_user(self, uuid: str) -> UserTable:
        """
        Retrieve a user instance from the database by UUID.

        Parameters:
            uuid (str): UUID-like string identifying the user.

        Returns:
            UserTable: User instance.
        """
        try:
            uuid = UUID(uuid)
        except ValueError:
            raise HTTPException(
                400, "Invalid UUID was provided."
            )
        
        scalar: UserTable = (await db.execute(
            select(UserTable)
                .where(UserTable.id == uuid)
                .options(selectinload("*"))
        )).scalar_one_or_none()

        if not scalar:
            raise HTTPException(401, "Invalid user ID was provided.")

        return scalar
    
    async def cabale_cookie_required(
        self, request: Request, 
        cabale_token: Union[str, None] = Depends(api_cabale)
    ):
        """
        Ensure that a valid Cabale token is present in the cookies.

        Parameters:
            request (Request): The request object.
            cabale_token (Union[str, None]): The Cabale token from the cookies.
        """
        if not cabale_token:
            raise HTTPException(401, "No Cabale token provided.")
        
        user: UserTable = await self.get_user(cabale_token.split(":@:")[0])
        verified = cabale.verify_cabale_token(cabale_token, b64decode(user.iv))
        _g = lambda key: verified.get(key, str)
        
        if not _g("uuid") and not _g("iat"):
            raise HTTPException(500, _g("detail"))
        
        if cabale._iat() - _g("iat") >= cabale.settings.max_age:
            raise HTTPException(401, "Expired credential.")
        
        request.state.cabale = verified
        request.state.user = user.to_dict()
        
    def set_pair(
        self, response: Response, 
        cabale_token: str
    ) -> None:
        """
        Set the Cabale token in the response cookies.

        Parameters:
            response (Response): The response object.
            cabale_token (str): The Cabale token to be set in the cookies.
        """
        response.set_cookie("cabale_token", cabale_token, max_age=cabale.settings.max_age, httponly=True)

cabale_auth = CabaleAuthManager()