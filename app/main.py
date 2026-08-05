from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine
from app.api import router
from app.core.exceptions import AppException
from app.core.exception_handlers import (
    app_exception_handler,
    validation_exception_handler,
    RequestValidationError,
    unexpected_exception_handler,
)

app = FastAPI()
app.include_router(router)
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



