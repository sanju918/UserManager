from fastapi import FastAPI

from .apis import generic
from .apis import user_router


def init_app():
    api_app = FastAPI(title="Async SQLAlchemy", description="Nothing", version="1")

    api_app.include_router(generic.router)
    api_app.include_router(user_router.router)

    return api_app


app = init_app()
