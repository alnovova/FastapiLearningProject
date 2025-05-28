from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from starlette import status
from starlette.responses import JSONResponse

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register")
async def register_user(data: UserRequestAdd):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    try:
        async with async_session_maker() as session:
            await UsersRepository(session).add(new_user_data)
            await session.commit()
    except IntegrityError:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({
                "detail": [
                    {
                        "loc": ["body", "email"],
                        "msg": "Email уже зарегистрирован",
                        "type": "value_error.unique"
                    }
                ]
            })
        )

    return {"status": "OK"}
