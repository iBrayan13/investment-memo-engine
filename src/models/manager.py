from enum import Enum
from typing import Optional, Literal, TypedDict, Dict, Any

from pydantic import BaseModel, Field

class StatusEnum(str, Enum):
    started = "started"
    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"

class Memo(TypedDict):
    memo_id: str
    status: StatusEnum
    status_message: str = Field(default="", description="Detailed status message in Spanish")
    memo_object: Dict[str, Any] = Field(default={}, description="The generated memo object")
    memo_file_path: Optional[str] = Field(default=None, description="Path to the generated memo DOCX file")