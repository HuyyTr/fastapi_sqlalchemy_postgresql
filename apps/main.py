from fastapi import FastAPI

from core.config import settings
from api.router import router

import uvicorn
from contextlib import asynccontextmanager


def init_routers(app: FastAPI):
    app.include_router(router, prefix=settings.environment.API_PREFIX)


@asynccontextmanager
async def lifespane(app: FastAPI):
    print("Initializing...")
    init_routers(app)
    yield
    print("Shutting down ...")


app = FastAPI(
    debug=settings.environment.DEBUG,
    lifespan=lifespane
)


def start():
    uvicorn.run("apps.main:app",
                host=settings.environment.SERVER_HOST,
                port=settings.environment.SERVER_PORT,
                log_level="info",
                reload=True)
