from pydantic import BaseModel, Field
from typing import Literal


class CodeRunRequest(BaseModel):
    language: Literal["python"]
    code: str = Field(description="Исходный код", examples=["print('Hello')"])


class CodeRunResponse(BaseModel):
    status: str
    job_name: str
    output: str
