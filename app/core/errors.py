from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = jsonable_encoder(exc.errors())
    clean_error = []
    for error in errors:
        tag = [tag_name for tag_name in error['loc'] if tag_name != 'body'][0]
        msg = error['msg']
        type_error = error['type']
        clean_error.append({
            'type': type_error,
            'tag': tag,
            'msg': msg
        })

    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "details": clean_error,
        }
    )