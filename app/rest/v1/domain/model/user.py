from uuid import uuid4

from passlib.context import CryptContext
from sqlalchemy import Column, String, Boolean
from app.core.database import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserModel(Base):
    id: str = Column(
        String(36),
        primary_key=True,
        index=True,
        nullable=False,
        default=uuid4().__str__(),
    )
    name: str = Column(String(50), nullable=False)
    email: str = Column(String(255), nullable=False)
    passwd: str = Column(String(255), nullable=False)
    is_active: bool = Column(Boolean, nullable=False, default=True)
    is_superuser: bool = Column(Boolean, nullable=False, default=False)

    @property
    def password(self) -> str:
        return self.passwd

    @password.setter
    def password(self, value) -> None:
        self.passwd = pwd_context.hash(value)

    def check_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.password)
