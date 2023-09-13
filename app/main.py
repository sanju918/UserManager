from fastapi import FastAPI
from .crud_apis import generic


def init_app():
    api_app = FastAPI(title="Async SQLAlchemy", description="Nothing", version="1")

    api_app.include_router(generic.router)

    return api_app


app = init_app()
