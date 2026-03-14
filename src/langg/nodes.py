import json
import logging

from src.langg.state import MemoState
from src.services.pchain.chainable import MinimalChainable
from src.core.settings import DevelopmentSettings as Settings
from src.services.pchain.chain_prompt_manager import ChainPromptManager, ClientPrompt
from src.langg.models import (
   ExceptionDict,
   GenericResponse,
   InvestmentMemo
)

logger = logging.getLogger(__name__)


class Nodes:
   def __init__(
      self,
      settings: Settings,
      minimal_chainable: MinimalChainable,
      prompt_manager: ChainPromptManager
   ) -> None:
      self.settings = settings
      self.minimal_chainable = minimal_chainable
      self.prompt_manager = prompt_manager

   def merge_inputs(self, state: MemoState):
      merged = {}

      for item in state["raw_inputs"]:
         merged.update(item)

      state["merged_input"] = merged

      return state
   
   async def extract_entities(self, state: MemoState):
      prompt = f"""
      Extract relevant investment information from the following data.

      Identify:
      - project name
      - location
      - asset type
      - acquisition price
      - deal structure
      - risks
      - financials
      - development plan

      Data:
      {state["merged_input"]}
      """

      responses = await self.minimal_chainable.run(
         client="openrouter",
         model="openai/gpt-4o-mini",
         prompts=[ClientPrompt(prompt=prompt)],
         returns_model={0: GenericResponse}
      )
      response: GenericResponse = responses[0].response

      state["extracted_entities"] = response.response_data

      return state
   
   async def normalize_data(self, state: MemoState):
      prompt = f"""
      Normalize this investment data into standard concepts.

      Use consistent keys.

      Data:
      {state["extracted_entities"]}
      """

      responses = await self.minimal_chainable.run(
         client="openrouter",
         model="openai/gpt-4o-mini",
         prompts=[ClientPrompt(prompt=prompt)],
         returns_model={0: GenericResponse}
      )
      response: GenericResponse = responses[0].response

      state["normalized_data"] = response.response_data

      return state
   
   async def financial_agent(self, state: MemoState):
      prompt = f"""
      From this investment data extract or infer financial structure.

      Return:
      - budget
      - revenues
      - NOI
      - IRR scenarios if possible

      Data:
      {state["normalized_data"]}
      """

      responses = await self.minimal_chainable.run(
         client="openrouter",
         model="openai/gpt-4o-mini",
         prompts=[ClientPrompt(prompt=prompt)],
         returns_model={0: GenericResponse}
      )
      response: GenericResponse = responses[0].response

      state["financial_analysis"] = response.response_data

      return state
   
   async def risk_agent(self, state: MemoState):
      prompt = f"""
      Identify all investment risks.

      Classify severity:
      - CRITICAL
      - HIGH
      - MEDIUM
      - LOW

      Provide mitigation suggestions.

      Data:
      {state["normalized_data"]}
      """

      responses = await self.minimal_chainable.run(
         client="openrouter",
         model="openai/gpt-4o-mini",
         prompts=[ClientPrompt(prompt=prompt)],
         returns_model={0: GenericResponse}
      )
      response: GenericResponse = responses[0].response

      state["risk_analysis"] = response.response_data

      return state
   
   async def build_memo(self, state: MemoState):
      prompt = f"""
      Build the final Investment Memo JSON using this schema.

      Use null if information is missing.

      Data:
      normalized: {state["normalized_data"]}
      financials: {state["financial_analysis"]}
      risks: {state["risk_analysis"]}
      """

      responses = await self.minimal_chainable.run(
         client="openrouter",
         model="openai/gpt-4o-mini",
         prompts=[ClientPrompt(prompt=prompt)],
         returns_model={0: GenericResponse}
      )
      response: GenericResponse = responses[0].response

      state["memo_json"] = response.response_data

      return state
   
   def validate_json(self, state: MemoState):
      try:

         InvestmentMemo(**state["memo_json"])

         state["validation_errors"] = []

      except Exception as e:

         state["validation_errors"] = [str(e)]

      return state