from typing import Literal

from pydantic import BaseModel, Field


class SAIRequest(BaseModel):
    type: Literal['text', 'audio'] = Field(
        ..., description='Type of the incoming payload'
    )
    data: str = Field(
        ..., description='Raw text prompt or URL to the audio file'
    )
