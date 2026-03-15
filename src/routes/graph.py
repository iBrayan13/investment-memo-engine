import json
import logging

from fastapi import APIRouter, Request, status

from src.langg.nodes import Nodes
from src.langg.state import MemoState
from src.langg.graph import WorkFlow, StateGraph
from src.services.pchain.chainable import MinimalChainable
from src.core.settings import DevelopmentSettings as Settings
from src.services.pchain.chain_prompt_manager import ChainPromptManager

logger = logging.getLogger(__name__)
settings = Settings()

graph_router = APIRouter(prefix="/graph", tags=["Graph"])

@graph_router.post("/", status_code=status.HTTP_200_OK)
async def call_graph():
    logger.info(f"Received request to call graph")

    workflow = WorkFlow(
        nodes=Nodes(
            settings=settings,
            minimal_chainable=MinimalChainable(settings=settings),
            prompt_manager=ChainPromptManager()
        ),
        state_graph=StateGraph(MemoState)
    )

    with open("deal_structure.json", "r") as f:
        deal_structure = json.loads(f.read())
    with open("property_overview.json", "r") as f:
        property_overview = json.loads(f.read())
    with open("risks.json", "r") as f:
        risks = json.loads(f.read())

    graph_result: MemoState =  await workflow.app.ainvoke(input={"raw_inputs": [deal_structure, property_overview, risks]})

    return {
        "data": graph_result["memo_request"].model_dump() if graph_result.get("memo_request") else None,
    }