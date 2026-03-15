from pydantic import BaseModel, Field

class MemoGenerateRequest(BaseModel):
    raw_inputs: list = Field(default_factory=list)