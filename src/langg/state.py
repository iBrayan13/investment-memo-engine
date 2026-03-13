from typing import TypedDict, List, Dict, Any

class MemoState(TypedDict):

    raw_inputs: List[Dict[str, Any]]

    merged_input: Dict[str, Any]

    extracted_entities: Dict[str, Any]

    normalized_data: Dict[str, Any]

    financial_analysis: Dict[str, Any]

    risk_analysis: List[Dict[str, Any]]

    memo_json: Dict[str, Any]

    validation_errors: List[str]