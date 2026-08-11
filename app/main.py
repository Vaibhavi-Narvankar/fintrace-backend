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
from sqlalchemy import text
from app.middleware.security_headers import security_headers_middleware
from fastapi.middleware.cors import CORSMiddleware

setup_logging()
app = FastAPI()
app.include_router(router)
app.middleware("http")(request_logging_middleware)
app.middleware("http")(security_headers_middleware)
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
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

@app.get("/")
async def test_db():
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        return {"message": "DB connected successfully"}
    except Exception as e:
        return {"error": str(e)}



