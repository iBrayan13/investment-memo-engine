import json
import logging
import datetime

from src.langg.state import MemoState
from src.services.memos_manager import MemosManager
from src.services.pchain.chainable import MinimalChainable
from src.core.settings import DevelopmentSettings as Settings
from src.services.pchain.chain_prompt_manager import ChainPromptManager, ClientPrompt
from src.models.manager import StatusEnum
from src.models.langg import (
   MemoRequest, InvestmentMemo, AcquisitionPrice, Financials,
   TotalPotentialLandCost, LegalExpenseFund, ClosingCosts,
   Risk, Asset, Comparable, Budget, Financing, Income, Returns, Structure, DueDiligence,
)
from src.models.pipeline_langg import (
   ExtractedEntities, NormalizedData,
   BudgetAnalysis, BudgetLine, IncomeAnalysis, ComparableItem, RiskAnalysis,
   NormalizedRisk,
)

logger = logging.getLogger(__name__)
MAX_RETRIES = 3


class Nodes:
    def __init__(
        self,
        settings: Settings,
        minimal_chainable: MinimalChainable,
        prompt_manager: ChainPromptManager,
        memos_manager: MemosManager,
    ) -> None:
        self.settings = settings
        self.minimal_chainable = minimal_chainable
        self.prompt_manager = prompt_manager
        self.memos_manager = memos_manager

    # ── 1. merge_inputs ──────────────────────────────────────────────────────

    def merge_inputs(self, state: MemoState):
        logger.info(f"Merging {len(state['raw_inputs'])} inputs")
        self.memos_manager.save_new_memo(memo_id=state["memo_id"])

        merged = {}
        for item in state["raw_inputs"]:
            merged.update(item)
        state["merged_input"] = merged

        self.memos_manager.update_memo_status(memo_id=state["memo_id"], status=StatusEnum.in_progress, status_message="Unificando datos fuente.")
        return state

    # ── 2. extract_entities → ExtractedEntities ──────────────────────────────

    async def extract_entities(self, state: MemoState):
        logger.info("Extracting entities")
        self.memos_manager.update_memo_message(memo_id=state["memo_id"], status_message="Extrayendo entidades clave de los datos fuente.")

        schema = json.dumps(ExtractedEntities.model_json_schema(), indent=2)
        prompt = f"""
        Extract ALL investment data from the source below.

        Return a single JSON object that strictly follows this schema.
        Every field in the schema is REQUIRED — do not use null.
        If a value is not explicit in the source, infer it from context.
        Return ONLY JSON, no markdown, no explanation.

        Schema:
        {schema}

        Source data:
        {state["merged_input"]}
        """
        responses = await self.minimal_chainable.run(
            client="openrouter",
            model="openai/gpt-4o-mini",
            prompts=[ClientPrompt(prompt=prompt)],
            returns_model={0: ExtractedEntities},
        )
        state["extracted_entities"] = responses[0].response
        return state

    # ── 3. normalize_data → NormalizedData ───────────────────────────────────

    async def normalize_data(self, state: MemoState):
        logger.info("Normalizing data")
        self.memos_manager.update_memo_message(memo_id=state["memo_id"], status_message="Normalizando datos.")

        schema = json.dumps(NormalizedData.model_json_schema(), indent=2)
        prompt = f"""
        Normalize this investment data. Every field is REQUIRED — do not use null.

        Rules:
        - Convert ALL monetary values to numbers in millions of COP.
          Examples: "COP $3,500 MM" → 3500.0 | "$5,000,000,000 COP" → 5000.0
        - acquisition_price_base and acquisition_price_max stay in full COP (not MM).
          Example: 3500000000.0
        - severity must be exactly one of: CRITICAL | HIGH | MEDIUM | LOW
        - If a monetary value is a range, use the midpoint.
        - Return ONLY JSON matching the schema, no markdown.

        Schema:
        {schema}

        Source:
        {state["extracted_entities"].model_dump()}
        """
        responses = await self.minimal_chainable.run(
            client="openrouter",
            model="openai/gpt-4o-mini",
            prompts=[ClientPrompt(prompt=prompt)],
            returns_model={0: NormalizedData},
        )
        state["normalized_data"] = responses[0].response
        return state

    # ── 4a. budget_agent → BudgetAnalysis ────────────────────────────────────

    async def budget_agent(self, state: MemoState):
        logger.info("Analyzing budget and financing structure")
        self.memos_manager.update_memo_message(memo_id=state["memo_id"], status_message="Analizando presupuesto y estructura de financiamiento.")

        schema = json.dumps(BudgetAnalysis.model_json_schema(), indent=2)
        nd = state["normalized_data"].model_dump()
        prompt = f"""
        Build the complete project budget and financing structure.
        Every field is REQUIRED — do not use null.

        Rules:
        - Monetary amounts as strings in MM COP (e.g. "3,500").
        - Percentages as strings with % sign (e.g. "15.9%").
        - land.amount_millions_cop must equal normalized base_purchase_price_millions_cop.
        - total_millions_cop must equal the sum of all budget lines.
        - equity_required_millions_cop + senior_debt_millions_cop must equal total_millions_cop.
        - If a budget line has no data, distribute proportionally using typical
          real estate development ratios for Colombia.
        - Return ONLY JSON matching the schema, no markdown.

        Schema:
        {schema}

        Data:
        {json.dumps(nd, indent=2)}
        """
        responses = await self.minimal_chainable.run(
            client="openrouter",
            model="openai/gpt-4o-mini",
            prompts=[ClientPrompt(prompt=prompt)],
            returns_model={0: BudgetAnalysis},
        )
        state["budget_analysis"] = responses[0].response
        return state

    # ── 4b. income_agent → IncomeAnalysis ────────────────────────────────────

    async def income_agent(self, state: MemoState):
        logger.info("Analyzing income, NOI and return scenarios")
        self.memos_manager.update_memo_message(memo_id=state["memo_id"], status_message="Analizando ingresos, NOI y escenarios de retorno.")

        schema = json.dumps(IncomeAnalysis.model_json_schema(), indent=2)
        nd = state["normalized_data"].model_dump()
        prompt = f"""
        Build the stabilized income statement, return scenarios, market context
        and GP/LP structure for this investment.
        Every field is REQUIRED — do not use null.

        Rules:
        - Monetary amounts as strings in MM COP (e.g. "4,800").
        - Percentages as strings with % (e.g. "10%").
        - IRR as string with % (e.g. "18%"), equity multiple as string (e.g. "2.1x").
        - EGI = gross_potential - vacancy. NOI = EGI - opex. These must be consistent.
        - gross_pct = 100% always. All other pct fields relative to gross_potential.
        - bear scenario: conservative assumptions (higher vacancy, lower exit cap rate).
        - base scenario: most likely case.
        - bull scenario: optimistic assumptions.
        - For GP/LP structure, use the deal_structure and development_plan context.
        - If exact values are not in the data, use market-standard assumptions
          for Colombian real estate (vacancy 10-15%, opex 35-40% of EGI).
        - comparables: provide market comparables for this asset type and location.
          If the input data contains real comparables, use them.
          If not, infer AT LEAST 1 plausible comparable from your knowledge of
          the Colombian real estate market for this asset type and location.
          Include up to 3 if you can reasonably support them.
        - market_fundamentals: describe supply/demand, vacancy rates, absorption
          and rental trends for this asset type and location.
        - competitive_advantages: explain what differentiates this asset
          from the comparables listed.
        - Return ONLY JSON matching the schema, no markdown.

        Schema:
        {schema}

        Data:
        {json.dumps(nd, indent=2)}
        """
        responses = await self.minimal_chainable.run(
            client="openrouter",
            model="openai/gpt-4o-mini",
            prompts=[ClientPrompt(prompt=prompt)],
            returns_model={0: IncomeAnalysis},
        )
        state["income_analysis"] = responses[0].response
        return state

    # ── 5. risk_agent → RiskAnalysis ─────────────────────────────────────────

    async def risk_agent(self, state: MemoState):
        logger.info("Analyzing risks and due diligence")
        self.memos_manager.update_memo_message(memo_id=state["memo_id"], status_message="Analizando riesgos y diligencia debida.")

        schema = json.dumps(RiskAnalysis.model_json_schema(), indent=2)
        nd = state["normalized_data"].model_dump()
        prompt = f"""
        Identify ALL investment risks and due diligence findings.
        Every field is REQUIRED — do not use null or empty strings.

        Rules:
        - severity must be exactly one of: CRITICAL | HIGH | MEDIUM | LOW
        - mitigation_strategy must be concrete and actionable, not generic.
        - dd_* fields: write the current status and key findings for each area.
          If no information is available for an area, write "Pendiente — no hay
          información disponible en los datos fuente."
        - conditions: at least 3 specific investment conditions based on the risks.
        - Return ONLY JSON matching the schema, no markdown.

        Schema:
        {schema}

        Data:
        {json.dumps(nd, indent=2)}
        """
        responses = await self.minimal_chainable.run(
            client="openrouter",
            model="openai/gpt-4o-mini",
            prompts=[ClientPrompt(prompt=prompt)],
            returns_model={0: RiskAnalysis},
        )
        state["risk_analysis"] = responses[0].response
        return state

    # ── 6. build_memo — ensambla desde modelos tipados, sin LLM ──────────────

    def build_memo(self, state: MemoState):
        logger.info("Assembling MemoRequest from typed models")
        self.memos_manager.update_memo_message(memo_id=state["memo_id"], status_message="Ensamblando el memorando de inversión final.")

        nd: NormalizedData = state["normalized_data"]
        ba: BudgetAnalysis = state["budget_analysis"]
        ia: IncomeAnalysis = state["income_analysis"]
        ra: RiskAnalysis   = state["risk_analysis"]

        state["memo_request"] = MemoRequest(
            investment_memo=InvestmentMemo(
                project_name=nd.project_name,
                location=nd.location,
                asset_type=nd.asset_type,
                deal_structure=nd.deal_structure,
                development_plan=nd.development_plan,
                acquisition_price=AcquisitionPrice(
                    base=nd.acquisition_price_base,
                    max_with_contingent=nd.acquisition_price_max,
                ),
                financials=Financials(
                    base_purchase_price_millions_cop=nd.base_purchase_price_millions_cop,
                    total_potential_land_cost=TotalPotentialLandCost(
                        minimum=nd.land_cost_min_millions_cop,
                        maximum=nd.land_cost_max_millions_cop,
                    ),
                    legal_expense_fund=LegalExpenseFund(
                        amount_millions_cop=nd.legal_fund_amount_millions_cop,
                        purpose=nd.legal_fund_purpose,
                    ),
                    closing_costs=ClosingCosts(
                        notary_fees=nd.notary_fees,
                        registration_fees=nd.registration_fees,
                        transfer_taxes=nd.transfer_taxes,
                    ),
                ),
                risks=[
                    Risk(
                        risk_description=r.risk_description,
                        severity=r.severity,
                        mitigation_strategy=r.mitigation_strategy,
                    )
                    for r in ra.risks
                ],
            ),
            # ── campos raíz ─────────────────────────────────────────────────
            prepared_by="Vertex Capital Group - Deal Team",
            date=str(datetime.date.today()),
            equity_required=ba.equity_required_millions_cop,
            total_project_cost=ba.total_millions_cop,
            recommendation="MÁS DD",        # siempre MÁS DD hasta validar legal
            executive_summary=(
                f"{nd.project_name} es un {nd.asset_type} ubicado en {nd.location}. "
                f"Estructura del deal: {nd.deal_structure}. "
                f"Costo total del proyecto: {ba.total_millions_cop} MM COP. "
                f"Equity requerido: {ba.equity_required_millions_cop} MM COP. "
                f"IRR base proyectado: {ia.base.irr}. "
                f"Riesgo principal: {ra.risks[0].risk_description if ra.risks else 'N/A'}."
            ),
            highlights=[
                f"Ubicación: {nd.location}",
                f"Tipo de activo: {nd.asset_type}",
                f"IRR base: {ia.base.irr} | Equity Multiple: {ia.base.equity_multiple}",
                f"Riesgo crítico: {next((r.risk_description for r in ra.risks if r.severity == 'CRITICAL'), 'Ninguno identificado')}",
            ],
            # ── asset (inferido desde normalized_data) ──────────────────────
            location_description=nd.location,
            asset=Asset(
                area_m2="Por determinar",
                units="N/A",
                zoning="Por confirmar",
                year_built="Nuevo – greenfield",
                status="En desarrollo",
                occupancy="0% – pre-construcción",
            ),
            market_fundamentals=ia.market_fundamentals,
            comparables=[
                Comparable(
                    project=c.project,
                    location=c.location,
                    rent_m2=c.rent_m2,
                    cap_rate=c.cap_rate,
                    year=c.year,
                )
                for c in ia.comparables
            ],
            competitive_advantages=ia.competitive_advantages,
            # ── financieros ──────────────────────────────────────────────────
            budget=Budget(
                land=ba.land.amount_millions_cop,       land_pct=ba.land.pct_of_total,
                hard_costs=ba.hard_costs.amount_millions_cop, hard_costs_pct=ba.hard_costs.pct_of_total,
                soft_costs=ba.soft_costs.amount_millions_cop, soft_costs_pct=ba.soft_costs.pct_of_total,
                contingency=ba.contingency.amount_millions_cop, contingency_pct=ba.contingency.pct_of_total,
                financing_costs=ba.financing_costs.amount_millions_cop, financing_costs_pct=ba.financing_costs.pct_of_total,
                legal_pct=ba.legal.pct_of_total,
                other=ba.other.amount_millions_cop,     other_pct=ba.other.pct_of_total,
                total=ba.total_millions_cop,
            ),
            financing=Financing(
                senior_debt_amount=ba.senior_debt_millions_cop,
                senior_debt_terms=ba.senior_debt_terms,
                equity_amount=ba.equity_required_millions_cop,
                equity_terms=ba.equity_terms,
            ),
            income=Income(
                gross_potential=ia.gross_potential_millions_cop, gross_pct=ia.gross_pct,
                vacancy=ia.vacancy_millions_cop,                  vacancy_pct=ia.vacancy_pct,
                egi=ia.egi_millions_cop,                          egi_pct=ia.egi_pct,
                opex=ia.opex_millions_cop,                        opex_pct=ia.opex_pct,
                noi=ia.noi_millions_cop,                          noi_pct=ia.noi_pct,
            ),
            returns=Returns(
                irr_bear=ia.bear.irr,   irr_base=ia.base.irr,   irr_bull=ia.bull.irr,
                em_bear=ia.bear.equity_multiple, em_base=ia.base.equity_multiple, em_bull=ia.bull.equity_multiple,
                coc_bear=ia.bear.cash_on_cash_yr3, coc_base=ia.base.cash_on_cash_yr3, coc_bull=ia.bull.cash_on_cash_yr3,
            ),
            structure=Structure(
                gp_capital=ia.gp_capital,        gp_terms=ia.gp_terms,
                lp_capital=ia.lp_capital,         lp_terms=ia.lp_terms,
                preferred_return=ia.preferred_return,
                promote_carry=ia.promote_carry,
                capital_calls_timeline=ia.capital_calls_timeline,
                governance=ia.governance,
            ),
            dd=DueDiligence(
                legal=ra.dd_legal,
                technical=ra.dd_technical,
                environmental=ra.dd_environmental,
                zoning=ra.dd_zoning,
                financial=ra.dd_financial,
                adverse_possession=ra.dd_adverse_possession,
            ),
            rationale=[
                f"Estructura de deal: {nd.deal_structure}",
                f"IRR base proyectado: {ia.base.irr} vs benchmark mercado 14-16%",
                f"Riesgo principal identificado y con plan de mitigación definido",
                f"Plan de desarrollo estructurado: {nd.development_plan[:100]}...",
            ],
            conditions=ra.conditions,
            next_steps=(
                "1. Completar DD legal (adverse possession). "
                "2. Auditoría tributaria. "
                "3. Confirmar modelo financiero con datos de mercado. "
                "4. Presentar resultado al comité en 30 días."
            ),
        )
        state["validation_errors"] = []
        return state

    # ── 7. build_memo_docx ─────────────────────────────────────────────────────

    def build_memo_docx(self, state: MemoState):
        logger.info("Building memo DOCX")
        self.memos_manager.update_memo_message(memo_id=state["memo_id"], status_message="Generando documento DOCX.")

        # TODO: implementar generación de DOCX usando python-docx o similar, con formato profesional

        state["memo_file_path"] = f"{state['memo_id']}.docx"
        self.memos_manager.update_memo_status(
            memo_id=state["memo_id"],
            status=StatusEnum.completed,
            status_message="Memo generado con exito.",
            memo_object=state["memo_request"].model_dump(),
            memo_file_path=state["memo_file_path"],
        )
        return state
    
    def mark_as_failed(self, state: MemoState):
        logger.error(f"Workflow failed")
        self.memos_manager.update_memo_status(
            memo_id=state["memo_id"],
            status=StatusEnum.failed,
            status_message="Error: Workflow failed",
        )
        return state