from typing_extensions import TypedDict, List, Dict, Any, Optional, Literal

from pydantic import BaseModel, Field

class ExceptionDict(TypedDict):
    exception_node: str
    exception_type: str
    exception_text: SyntaxWarning
    end: bool

class InvestmentMemo(BaseModel):
    memo_metadata: dict
    investment_overview: dict
    business_or_asset_description: dict
    market_analysis: dict
    financial_analysis: dict
    deal_structure: dict
    risk_analysis: list

class GenericResponse(BaseModel):
    success: bool
    response_data: Dict[str, Any]