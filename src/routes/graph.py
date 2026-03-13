import logging

from fastapi import APIRouter, Request

from src.langg.nodes import Nodes
from src.langg.state import State
from src.langg.graph import WorkFlow, StateGraph
from src.services.pchain.chainable import MinimalChainable
from src.core.settings import DevelopmentSettings as Settings
from src.services.pchain.chain_prompt_manager import ChainPromptManager

logger = logging.getLogger(__name__)
settings = Settings()

graph_router = APIRouter(prefix="/graph", tags=["Graph"])

@graph_router.post("/")
async def call_graph():
    logger.info(f"Received request to call graph")

    workflow = WorkFlow(
        nodes=Nodes(
            settings=settings,
            minimal_chainable=MinimalChainable(settings=settings),
            prompt_manager=ChainPromptManager()
        ),
        state_graph=StateGraph(State)
    )

    graph_result: State =  await workflow.app.ainvoke(input={})

    return {
        "call_outcome": graph_result["call_outcome"]
    }