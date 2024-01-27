from typing import List, Dict

from pydantic import BaseModel, Field


class AdetailerModelResponse(BaseModel):
    modles: List[str] = Field(
        title='Models',
        description='The models.'
    )
