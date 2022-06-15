from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND

from app.rest.v1.presentation.controller.user import UserController
from app.core.database import get_session
from app.rest.v1.domain.entity.user import UserCreateEntity, UserEntity, UserPatchEntity

router = APIRouter(prefix="/user", tags=["User"])


@router.get(path="/", response_model=Union[UserEntity, List[UserEntity]])
async def get(
        id: str
            | None = Query(
            None,
            required=False,
            min_length=36,
            max_length=36,
            example="fe96132e-57a4-4f40-8044-3d0c82bc8521",
        ),
        name: str | None = None,
        email: str | None = None,
        is_active: bool | None = None,
        is_superuser: bool | None = None,
        session: Session = Depends(get_session),
):
    controller = UserController()
    user = await controller.get(
        session=session,
        id=id,
        name=name,
        email=email,
        is_active=is_active,
        is_superuser=is_superuser,
    )
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.patch(path="/{id}", response_model=UserEntity)
async def patch(
        data: UserPatchEntity,
        id: str = Query(
            ...,
            min_length=36,
            max_length=36,
            example="fe96132e-57a4-4f40-8044-3d0c82bc8521",
        ),
        session: Session = Depends(get_session),
):
    controller = UserController()
    user = await controller.get(session=session, id=id, as_list=False)
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")

    user = await controller.update(session=session, user=user, entity=data)
    return user


@router.post(path="/", response_model=UserEntity, status_code=HTTP_201_CREATED)
async def post(
        entity: UserCreateEntity,
        session: Session = Depends(get_session),
):
    controller = UserController()
    user = await controller.create(session=session, entity=entity)
    return user


@router.delete(
    path="/{id}",
    responses={
        HTTP_404_NOT_FOUND: {"detail": "User not found"},
        HTTP_200_OK: {"detail": "User deleted successfully"},
    },
)
async def delete(id: str, session: Session = Depends(get_session)):
    controller = UserController()
    user = await controller.get(session=session, id=id, as_list=False)
    if not user or not user.is_superuser:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")

    await controller.delete(session=session, user=user)
    return JSONResponse(
        status_code=HTTP_200_OK, content={"detail": "User deleted successfully"}
    )
