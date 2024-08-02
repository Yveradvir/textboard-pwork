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
    body: AuthBodyModel,
    session: AsyncSession = Depends(db.get_session)
):
    user = await get_scalar(
        session,
        select(UserTable).where(UserTable.username == body.username)
    )

    if user is None or not Hash.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    iv = cabale_auth.generate_iv()
    user.iv = iv
    await session.commit()
    
    print(iv, cabale_auth.decode_iv(iv))
    cabale_token = cabale.generate_cabale_token({}, str(user.id), cabale_auth.decode_iv(iv))  
    response = JSONResponse(
        content={"cabale": cabale_token},
        status_code=200
    )
    
    cabale_auth.set_cabale(response, cabale_token)
    
    return response

@router.post("/signup")
async def auth_signup(
    body: AuthBodyModel,
    session: AsyncSession = Depends(db.get_session)
):
    user_check = await get_scalar(
        session,
        select(UserTable).where(UserTable.username == body.username)
    )

    if user_check is not None:
        raise HTTPException(
            status_code=409,
            detail="This username is arleady taken"
        )

    iv = cabale_auth.generate_iv()

    body = body.model_dump()
    body["iv"] = iv
    body["password"] = Hash.get_password_hash(body["password"])
    
    user = UserTable(**body)

    session.add(user)
    await session.commit()
    await session.refresh(user)
    
    print(iv, cabale_auth.decode_iv(user.iv))
    cabale_token = cabale.generate_cabale_token({}, str(user.id), cabale_auth.decode_iv(user.iv))  
    response = JSONResponse(
        content={"cabale": cabale_token},
        status_code=200
    )
    
    cabale_auth.set_cabale(response, cabale_token)
    
    return response

@router.get("/", dependencies=[Depends(cabale_auth.cabale_cookie_required)])
def _(request: Request):
    return JSONResponse(request.state.cabale)