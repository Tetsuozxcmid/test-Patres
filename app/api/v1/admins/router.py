from fastapi import APIRouter, HTTPException, Response, status, Depends
from api.v1.admins.passlogic import pass_settings
from sqlalchemy.future import select
from api.v1.admins.auth import create_access_token
from schemas.librarian import LibrarianAuth, LibrarianRegister
from sqlalchemy.ext.asyncio import AsyncSession
from models.admin.librarian import librarian
from core.database.db import get_db


router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post("/register/")
async def register_user(user_data: LibrarianRegister, db: AsyncSession = Depends(get_db)) -> dict:
    existing_user = await db.execute(select(librarian).where(librarian.email == user_data.email))

    if existing_user.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    password_str = user_data.password.get_secret_value()
    hashed_password = pass_settings.get_password_hash(password_str)

    user_dict = user_data.dict(exclude={"password"})
    user_dict['hashed_password'] = hashed_password

    new_user = librarian(**user_dict)

    db.add(new_user)

    await db.commit()

    await db.refresh(new_user)

    return {
        "message": "User created successfully",
        "user_id": new_user.id,
        "email": new_user.email
    }


@router.post("/login/")
async def auth_user(response: Response, user_data: LibrarianAuth, db: AsyncSession = Depends(get_db)) -> dict:

    password_str = user_data.password.get_secret_value()
    user = await librarian.check_user(email=user_data.email, password=password_str, db=db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверная почта или пароль")

    access_token = await create_access_token({"sub": str(user['id'])})
    response.set_cookie(key="users_access_token",
                        value=access_token, httponly=True)
    return {'access_token': access_token, 'refresh_token': None}
