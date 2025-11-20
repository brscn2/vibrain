from fastapi import FastAPI

from .api.routes import health
from .cache.redis import close_redis_connection, connect_to_redis
from .core.config import settings
from .db.mongo import close_mongo_connection, connect_to_mongo


def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.project_name,
        version=settings.version,
    )

    app.add_event_handler("startup", connect_to_mongo)
    app.add_event_handler("shutdown", close_mongo_connection)

    app.add_event_handler("startup", connect_to_redis)
    app.add_event_handler("shutdown", close_redis_connection)

    app.include_router(health.router, prefix="/api")
    return app


app = create_application()
