from typing import Any, Dict

import arrow
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

from app.rest.v1.presentation.controller.user import UserController
from app.core.settings import settings
from app.rest.v1.domain.model.user import UserModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


class AuthController:
    """Service to provide an interface for authentication methods"""

    def __init__(self) -> None:
        pass

    def authenticate(self, user: UserModel, password: str) -> bool:
        """Check if provided password is the same as the user password
        Args:
            user: UserModel
            password: str
        Returns:
            bool
        """
        return user.check_password(plain_password=password)

    @staticmethod
    async def create_access_token(data: dict, expires_in: int | None = None) -> str:
        """Create access token (JWT)
        Args:
            data: dict
            expires_in: int | None
        Returns:
            str
        """
        to_encode = data.copy()

        expires_in = (
            expires_in if expires_in else settings.auth.access_token_expire_minutes
        )
        expire = arrow.get().shift(minutes=+expires_in)

        to_encode.update({"exp": expire.timestamp()})
        encoded = jwt.encode(
            to_encode, settings.auth.secret_key, algorithm=settings.auth.algorithm
        )
        return encoded

    async def decode_access_token(
        self, session: Session, token: str = Depends(oauth2_scheme)
    ) -> Dict[str, Any] | UserModel | Exception:
        """Decode access token (JWT)
        Args:
            session: Session
            token: str
        Returns:
            Dict[str, Any] | UserModel | Exception
        """
        credentials_exception = HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token, settings.auth.secret_key, algorithms=[settings.auth.algorithm]
            )
            id: str = payload.get("sub")
            if not id:
                raise credentials_exception

        except JWTError:
            raise credentials_exception

        controller = UserController()
        user = await controller.get(session=session, id=id, as_list=False)
        if not user:
            raise credentials_exception
        return user
