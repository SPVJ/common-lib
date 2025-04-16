
from fastapi import Request, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fsCommonLib.handlers.genericException import GenericException

async def validationExceptionHandler(request: Request, ex: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"message" : "wrong input handled"}
    )

async def genericExceptionHandler(request: Request, ex: GenericException):
    return JSONResponse(
        status_code= ex.status_code,
        content={"status_code" : ex.err_code,
                 "description ": ex.description}
    )

def addExceptionHandler(app: FastAPI):
    app.add_exception_handler(handler=validationExceptionHandler, exc_class_or_status_code=RequestValidationError)
    app.add_exception_handler(handler=genericExceptionHandler, exc_class_or_status_code=GenericException)
    return app
