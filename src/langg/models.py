from typing_extensions import TypedDict, List, Dict, Any, Optional, Literal

from pydantic import BaseModel, Field

class ExceptionDict(TypedDict):
    exception_node: str
    exception_type: str
    exception_text: SyntaxWarning
    end: bool
