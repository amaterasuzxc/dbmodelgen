from pydantic import BaseModel


class ProcessingResponseDto(BaseModel):
    model: str | None = None