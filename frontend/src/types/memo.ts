export type MemoStatus = 'started' | 'in_progress' | 'completed' | 'failed';

export interface Comparable {
  project: string;
  location: string;
  rent_m2: string;
  cap_rate: string;
  year: string;
}

export interface Budget {
  land: string;
  land_pct: string;
  hard_costs: string;
  hard_costs_pct: string;
  soft_costs: string;
  soft_costs_pct: string;
  contingency: string;
  contingency_pct: string;
  financing_costs: string;
  financing_costs_pct: string;
  legal_pct: string;
  other: string;
  other_pct: string;
  total: string;
}

export interface Financing {
  senior_debt_amount: string;
  senior_debt_terms: string;
  equity_amount: string;
  equity_terms: string;
}

export interface Returns {
  irr_bear: string;
  irr_base: string;
  irr_bull: string;
  em_bear: string;
  em_base: string;
  em_bull: string;
  coc_bear: string;
  coc_base: string;
  coc_bull: string;
}

export interface Risk {
  risk_description: string;
  severity: string;
  mitigation_strategy: string;
}

export interface DueDiligence {
  legal: string;
  technical: string;
  environmental: string;
  zoning: string;
  financial: string;
  adverse_possession: string;
}

export interface AssetInformation {
  area_m2: string;
  units: string;
  zoning: string;
  year_built: string;
  status: string;
  occupancy: string;
}

export interface Income {
  gross_potential: string;
  gross_pct: string;
  vacancy: string;
  vacancy_pct: string;
  egi: string;
  egi_pct: string;
  opex: string;
  opex_pct: string;
  noi: string;
  noi_pct: string;
}

export interface DealStructure {
  gp_capital: string;
  gp_terms: string;
  lp_capital: string;
  lp_terms: string;
  preferred_return: string;
  promote_carry: string;
  capital_calls_timeline: string;
  governance: string;
}

export interface InvestmentMemoCore {
  project_name: string;
  location: string;
  asset_type: string;
  acquisition_price?: {
    base: number;
    max_with_contingent: number;
  };
  deal_structure: string;
  risks: Risk[];
  financials?: Record<string, unknown>;
  development_plan?: string;
}

export interface MemoObject {
  investment_memo: InvestmentMemoCore;
  prepared_by: string;
  date: string;
  equity_required: string;
  total_project_cost: string;
  recommendation: string;
  executive_summary: string;
  highlights: string[];
  location_description: string;
  asset: AssetInformation;
  market_fundamentals: string;
  comparables: Comparable[];
  competitive_advantages: string;
  budget: Budget;
  financing: Financing;
  income: Income;
  returns: Returns;
  structure: DealStructure;
  dd: DueDiligence;
  rationale: string[];
  conditions: string[];
  next_steps: string;
}

export interface Memo {
  memo_id: string;
  status: MemoStatus;
  status_message: string;
  memo_file_path?: string;
  memo_object?: MemoObject;
}

export interface ApiListResponse {
  data: Memo[];
}

export interface GenerateResponse {
  memo_id: string;
  message: string;
}

export interface RawInput {
  type: string;
  data: Record<string, unknown>;
}
