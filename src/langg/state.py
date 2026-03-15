from typing import Optional, Annotated
from typing_extensions import TypedDict

from src.langg.models import MemoRequest
from src.langg.pipeline_models import (
    ExtractedEntities,
    NormalizedData,
    BudgetAnalysis,
    IncomeAnalysis,
    RiskAnalysis,
)


def _keep_last(current, new):
    return new


class MemoState(TypedDict, total=False):
    raw_inputs:           Annotated[list[dict],                   _keep_last]
    merged_input:         Annotated[dict,                         _keep_last]
    extracted_entities:   Annotated[Optional[ExtractedEntities],  _keep_last]
    normalized_data:      Annotated[Optional[NormalizedData],     _keep_last]
    budget_analysis:      Annotated[Optional[BudgetAnalysis],     _keep_last]
    income_analysis:      Annotated[Optional[IncomeAnalysis],     _keep_last]
    risk_analysis:        Annotated[Optional[RiskAnalysis],       _keep_last]
    memo_request:         Annotated[Optional[MemoRequest],        _keep_last]
    validation_errors:    Annotated[list[str],                    _keep_last]
    retry_count:          Annotated[int,                          _keep_last]