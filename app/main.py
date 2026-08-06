from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine
from app.api import router
from app.core.exceptions import AppException
from app.core.logging_config import setup_logging
from app.core.exception_handlers import (
    app_exception_handler,
    validation_exception_handler,
    RequestValidationError,
    unexpected_exception_handler,
)
from app.middleware.request_logging import request_logging_middleware

setup_logging()
app = FastAPI()
app.include_router(router)
app.middleware("http")(request_logging_middleware)
app.add_exception_handler(
    AppException,
    app_exception_handler
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

app.add_exception_handler(
    Exception,
    unexpected_exception_handler
)

@app.get("/")
def test_db():
    try:
        connection = engine.connect()
        connection.close()
        return {"message": "DB connected successfully"}
    except Exception as e:
        return {"error": str(e)}



