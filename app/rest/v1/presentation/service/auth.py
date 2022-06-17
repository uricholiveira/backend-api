from typing import Any, Dict

from fastapi import Depends
from sqlalchemy.orm import Session

from app.rest.v1.domain.model import UserModel
from app.rest.v1.presentation.controller.auth import AuthController, oauth2_scheme


class AuthService:
    """Future functions/methods that use more than one controller will be created here"""

    def __init__(self):
        self.controller = AuthController()

    def get_user_by_acess_token(
        self, session: Session, token: str = Depends(oauth2_scheme)
    ) -> Dict[str, Any] | UserModel | Exception:
        """Decode access token (JWT)
        Args:
            session: Session
            token: str
        Returns:
            Dict[str, Any] | UserModel | Exception
        """
        pass
