from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exceptions import AppException
from fastapi.exceptions import RequestValidationError

async def app_exception_handler(
    request: Request,
    exc: AppException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message,
        }
    )

async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    errors = []

    for error in exc.errors():
        field = ".".join(
            str(item)
            for item in error["loc"]
            if item != "body"
        )

        errors.append({
            "field": field,
            "message": error["msg"],
        })

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation failed",
            "errors": errors,
        }
    )