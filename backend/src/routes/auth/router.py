from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import Hash, cabale, cabale_auth

from src.routes.auth.models import AuthBodyModel
from src.core.utils.get_scalar import get_scalar
from src.database import db
from src.database.user import UserTable



router = APIRouter(prefix="/a", tags=["auth"])

@router.post("/signin")
async def auth_signin(
    request: Request,
    body: AuthBodyModel,
    db: AsyncSession = Depends(db.get_session)
):
    user = await get_scalar(
        db,
        select(UserTable).where(UserTable.username == body.username)
    )

    if user is None or not Hash.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    cabale_token = "example_token"  
    
    return JSONResponse(
        content={"cabale": cabale_token},
        status_code=200
    )
