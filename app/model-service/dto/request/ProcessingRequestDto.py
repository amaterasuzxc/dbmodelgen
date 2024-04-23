from pydantic import BaseModel


class ProcessingRequestDto(BaseModel):
    text: str