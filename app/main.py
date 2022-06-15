from fastapi import FastAPI

from app.core.settings import settings
from app.rest.common.middleware import middlewares
from app.rest.v1.router import routers

app = FastAPI(
    title=settings.app.title,
    description=settings.app.description,
    version=settings.app.version,
)

for router in routers:
    app.include_router(router=router)

for middleware in middlewares:
    app.add_middleware(middleware_class=middleware)
