from typing import Optional, Literal

from pydantic import BaseModel, Field


# ── extract_entities ──────────────────────────────────────────────────────────

class RawRisk(BaseModel):
    description: str
    severity_hint: str
    mitigation_hint: Optional[str] = None


class ExtractedEntities(BaseModel):
    project_name: str
    location: str
    asset_type: str
    deal_structure: str
    development_plan: str

    acquisition_price_base_raw: str
    acquisition_price_max_raw: str
    base_purchase_price_raw: str
    land_cost_min_raw: str
    land_cost_max_raw: str
    legal_fund_amount_raw: str
    legal_fund_purpose: str
    notary_fees: str
    registration_fees: str
    transfer_taxes: str

    risks: list[RawRisk] = Field(min_length=1)
    extra: dict = Field(default_factory=dict)


# ── normalize_data ────────────────────────────────────────────────────────────

class NormalizedRisk(BaseModel):
    risk_description: str
    severity: Literal["CRITICAL", "HIGH", "MEDIUM", "LOW"]
    mitigation_strategy: str


class NormalizedData(BaseModel):
    project_name: str
    location: str
    asset_type: str
    deal_structure: str
    development_plan: str

    acquisition_price_base: float
    acquisition_price_max: float
    base_purchase_price_millions_cop: float
    land_cost_min_millions_cop: float
    land_cost_max_millions_cop: float
    legal_fund_amount_millions_cop: float
    legal_fund_purpose: str
    notary_fees: str
    registration_fees: str
    transfer_taxes: str

    risks: list[NormalizedRisk] = Field(min_length=1)


# ── budget_agent ──────────────────────────────────────────────────────────────

class BudgetLine(BaseModel):
    amount_millions_cop: str
    pct_of_total: str


class BudgetAnalysis(BaseModel):
    land: BudgetLine
    hard_costs: BudgetLine
    soft_costs: BudgetLine
    contingency: BudgetLine
    financing_costs: BudgetLine
    legal: BudgetLine
    other: BudgetLine
    total_millions_cop: str

    equity_required_millions_cop: str
    senior_debt_millions_cop: str
    senior_debt_terms: str
    equity_terms: str


# ── income_agent ──────────────────────────────────────────────────────────────

class ReturnScenario(BaseModel):
    irr: str
    equity_multiple: str
    cash_on_cash_yr3: str


class ComparableItem(BaseModel):
    """
    Comparable de mercado.
    Si no hay datos reales en el input, el LLM los infiere desde su
    conocimiento del mercado para el asset_type y location del deal.
    """
    project: str
    location: str
    rent_m2: str
    cap_rate: str
    year: str


class IncomeAnalysis(BaseModel):
    gross_potential_millions_cop: str
    gross_pct: str
    vacancy_millions_cop: str
    vacancy_pct: str
    egi_millions_cop: str
    egi_pct: str
    opex_millions_cop: str
    opex_pct: str
    noi_millions_cop: str
    noi_pct: str

    bear: ReturnScenario
    base: ReturnScenario
    bull: ReturnScenario

    gp_capital: str
    gp_terms: str
    lp_capital: str
    lp_terms: str
    preferred_return: str
    promote_carry: str
    capital_calls_timeline: str
    governance: str

    # El LLM los extrae del input si existen, o los infiere del mercado
    comparables: list[ComparableItem] = Field(min_length=1)
    market_fundamentals: str
    competitive_advantages: str


# ── risk_agent ────────────────────────────────────────────────────────────────

class RiskAnalysis(BaseModel):
    risks: list[NormalizedRisk] = Field(min_length=1)

    dd_legal: str
    dd_technical: str
    dd_environmental: str
    dd_zoning: str
    dd_financial: str
    dd_adverse_possession: str

    conditions: list[str] = Field(min_length=1)