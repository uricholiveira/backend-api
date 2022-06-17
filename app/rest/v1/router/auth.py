from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)

from app.core.database import get_session
from app.rest.v1.domain.entity.auth import Token
from app.rest.v1.presentation.controller.auth import AuthController, oauth2_scheme
from app.rest.v1.presentation.controller.user import UserController

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get(
    path="/",
    responses={
        HTTP_404_NOT_FOUND: {"detail": "User not found"},
        HTTP_401_UNAUTHORIZED: {"detail": "Incorrect username or password"},
        HTTP_200_OK: {"detail": "User authenticated"},
    },
)
async def authenticate(
    email: EmailStr = Query(
        ...,
        example="email@yopmail.com",
    ),
    password: str = None,
    session: Session = Depends(get_session),
    controller: AuthController = Depends(AuthController),
    user_controller: UserController = Depends(UserController),
):
    user = await user_controller.get(session=session, email=email, as_list=False)
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")

    if controller.authenticate(user=user, password=password):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return JSONResponse(
        content={"detail": "User authenticated"}, status_code=HTTP_200_OK
    )


@router.post(
    path="/token",
    responses={
        HTTP_404_NOT_FOUND: {"detail": "User not found"},
        HTTP_401_UNAUTHORIZED: {
            "detail": "Incorrect username or password",
            "headers": {"WWW-Authenticate": "Bearer"},
        },
        HTTP_200_OK: {"access_token": "", "token_type": ""},
    },
    response_model=Token,
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
    controller: AuthController = Depends(AuthController),
    user_controller: UserController = Depends(UserController),
):
    user = await user_controller.get(
        session=session, email=form_data.username, as_list=False
    )

    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")

    if not controller.authenticate(user=user, password=form_data.password):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = await controller.create_access_token(
        data={
            "sub": user.id,
            "user": {"id": user.id, "email": user.email},
        }
    )
    return Token(**{"access_token": access_token, "token_type": "bearer"})


@router.post(
    path="/token/test",
    responses={
        HTTP_404_NOT_FOUND: {"detail": "User not found"},
        HTTP_400_BAD_REQUEST: {"detail": "User not authenticated"},
        HTTP_200_OK: {"detail": "User authenticated"},
    },
)
async def test(
    access_token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
    controller: AuthController = Depends(AuthController),
) -> JSONResponse:
    user = await controller.decode_access_token(session=session, token=access_token)
    if user:
        print(f"User logged in: {user.id}")
        return JSONResponse(
            content={"detail": "User authenticated"}, status_code=HTTP_200_OK
        )
    return JSONResponse(
        content={"detail": "User not authenticated"}, status_code=HTTP_403_FORBIDDEN
    )
