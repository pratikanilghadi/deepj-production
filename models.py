from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, Literal

def to_camel(string: str) -> str:
    """Converts snake_case_string to camelCaseString."""
    words = string.split('_')
    # The first word is lowercased, and all subsequent words are capitalized.
    return words[0] + ''.join(word.capitalize() for word in words[1:])

class APIBaseModel(BaseModel):
    class Config:
        # This configuration now correctly maps between JSON camelCase and Python snake_case
        alias_generator = to_camel
        populate_by_name = True

class RequestMetadata(APIBaseModel):
    file_type: str
    file_name: str
    original_file_id: str
    file_size: Optional[int] = None

class ProcessingRequest(APIBaseModel):
    job_id: str
    user_id: str
    input_file_url: HttpUrl
    output_file_url: HttpUrl
    processing_type: Literal["MELODYGEN"]
    metadata: RequestMetadata

class SuccessResponse(APIBaseModel):
    success: bool = True
    message: str
    job_id: str

class ErrorResponse(APIBaseModel):
    success: bool = False
    message: str
    error: Optional[str] = None

class StatusUpdateRequest(APIBaseModel):
    user_id: str
    file_id: str
    status: Literal["processing", "completed", "failed"]
    progress: int = Field(..., ge=0, le=100)
    message: str
    size: Optional[int] = None # Final MIDI file size in bytes
    python_job_id: str