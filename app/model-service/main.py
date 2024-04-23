from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from exceptions.MsConflictError import MsConflictError
from exceptions.MsInternalError import MsInternalError
from services.ModelService import ModelService
from dto.request.ProcessingRequestDto import ProcessingRequestDto
from dto.response.ProcessingResponseDto import ProcessingResponseDto


app = FastAPI()
model_service = ModelService()


@app.exception_handler(MsConflictError)
def conflict_handler(request: Request, ex: MsConflictError):
    return JSONResponse(
        status_code=409,
        content={"message": ex.message}
    )


@app.exception_handler(MsInternalError)
def generic_handler(request: Request, ex: MsInternalError):
    return JSONResponse(
        status_code=500,
        content={"message": ex.message | "Something went wrong"}
    )


@app.get("/healthcheck")
def healthcheck():
    return {}


@app.get("/apply")
def apply_model(request: ProcessingRequestDto) -> ProcessingResponseDto:
    text = ""
    try:
        text = request.text
    except Exception:
        raise MsInternalError()
    
    result = model_service.get_model_response(text)

    return ProcessingResponseDto(model=result)