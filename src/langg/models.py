from typing import Literal

from pydantic import BaseModel, Field


class AcquisitionPrice(BaseModel):
    base: float
    max_with_contingent: float


class TotalPotentialLandCost(BaseModel):
    minimum: float
    maximum: float


class LegalExpenseFund(BaseModel):
    amount_millions_cop: float
    purpose: str


class ClosingCosts(BaseModel):
    notary_fees: str
    registration_fees: str
    transfer_taxes: str


class Financials(BaseModel):
    base_purchase_price_millions_cop: float
    total_potential_land_cost: TotalPotentialLandCost
    legal_expense_fund: LegalExpenseFund
    closing_costs: ClosingCosts


class Risk(BaseModel):
    risk_description: str
    severity: Literal["CRITICAL", "HIGH", "MEDIUM", "LOW"]
    mitigation_strategy: str


class InvestmentMemo(BaseModel):
    project_name: str
    location: str
    asset_type: str
    acquisition_price: AcquisitionPrice
    deal_structure: str
    risks: list[Risk] = Field(min_length=1)
    financials: Financials
    development_plan: str


class Asset(BaseModel):
    area_m2: str
    units: str
    zoning: str
    year_built: str
    status: str
    occupancy: str


class Comparable(BaseModel):
    project: str
    location: str
    rent_m2: str
    cap_rate: str
    year: str


class Budget(BaseModel):
    land: str
    land_pct: str
    hard_costs: str
    hard_costs_pct: str
    soft_costs: str
    soft_costs_pct: str
    contingency: str
    contingency_pct: str
    financing_costs: str
    financing_costs_pct: str
    legal_pct: str
    other: str
    other_pct: str
    total: str


class Financing(BaseModel):
    senior_debt_amount: str
    senior_debt_terms: str
    equity_amount: str
    equity_terms: str


class Income(BaseModel):
    gross_potential: str
    gross_pct: str
    vacancy: str
    vacancy_pct: str
    egi: str
    egi_pct: str
    opex: str
    opex_pct: str
    noi: str
    noi_pct: str


class Returns(BaseModel):
    irr_bear: str
    irr_base: str
    irr_bull: str
    em_bear: str
    em_base: str
    em_bull: str
    coc_bear: str
    coc_base: str
    coc_bull: str


class Structure(BaseModel):
    gp_capital: str
    gp_terms: str
    lp_capital: str
    lp_terms: str
    preferred_return: str
    promote_carry: str
    capital_calls_timeline: str
    governance: str


class DueDiligence(BaseModel):
    legal: str
    technical: str
    environmental: str
    zoning: str
    financial: str
    adverse_possession: str


class MemoRequest(BaseModel):
    investment_memo: InvestmentMemo

    prepared_by: str
    date: str
    equity_required: str
    total_project_cost: str
    recommendation: Literal["INVERTIR", "PASAR", "MÁS DD"]

    executive_summary: str
    highlights: list[str] = Field(min_length=1)

    location_description: str
    asset: Asset
    market_fundamentals: str
    comparables: list[Comparable] = Field(min_length=1)
    competitive_advantages: str

    budget: Budget
    financing: Financing
    income: Income
    returns: Returns
    structure: Structure
    dd: DueDiligence

    rationale: list[str] = Field(min_length=1)
    conditions: list[str] = Field(min_length=1)
    next_steps: str