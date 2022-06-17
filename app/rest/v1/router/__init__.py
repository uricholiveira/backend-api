from typing import List

from fastapi import APIRouter

from . import auth, user

routers: List[APIRouter] = [user.router, auth.router]
