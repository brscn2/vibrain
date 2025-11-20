from fastapi import FastAPI

from .api.routes import health
from .core.config import settings


def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.project_name,
        version=settings.version,
    )

    app.include_router(health.router, prefix="/api")
    return app


app = create_application()
