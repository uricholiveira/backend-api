from typing import List

from sqlalchemy.orm import Session

from app.rest.v1.domain.entity.user import UserCreateEntity, UserPatchEntity
from app.rest.v1.domain.model.user import UserModel


class UserController:
    def __init__(self) -> None:
        pass

    async def get(
        self,
        session: Session,
        id: str | None = None,
        name: str | None = None,
        email: str | None = None,
        is_active: bool | None = None,
        is_superuser: bool | None = None,
        as_list: bool | None = True,
    ) -> List[UserModel] | UserModel:
        query = session.query(UserModel)

        if id:
            query.filter(UserModel.id == id)

        if name:
            query.filter(UserModel.name.like("%{}%".format(name)))

        if email:
            query.filter(UserModel.email == email)

        if is_active in (True, False):
            query.filter(UserModel.is_active == is_active)

        if is_superuser in (True, False):
            query.filter(UserModel.is_superuser == is_superuser)

        result = query.first() if not as_list else query.all()
        return result

    async def create(
        self, session: Session, entity: UserCreateEntity, **kwargs
    ) -> UserModel:
        """ "No one rule needs to be executed here, so we add and commit only"""
        user = UserModel(**entity.dict())

        session.add(user)
        session.commit()
        return user

    async def update(
        self, session: Session, user: UserModel, entity: UserPatchEntity
    ) -> UserModel:
        """ "No one rule needs to be executed here, so we add and commit only"""
        for k, v in entity.dict(exclude_unset=True).items():
            setattr(user, k, v)

        session.add(user)
        session.commit()
        return user

    async def override(self, session: Session, user: UserModel, **kwargs) -> UserModel:
        """ "No one rule needs to be executed here, so we add and commit only"""
        pass

    async def delete(self, session: Session, user: UserModel, **kwargs) -> None:
        """ "No one rule needs to be executed here, so we delete and commit only"""
        session.delete(user)
        session.commit()
