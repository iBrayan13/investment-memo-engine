from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from src.langg.nodes import Nodes, MAX_RETRIES
from src.langg.state import MemoState


class WorkFlow:
    def __init__(self, nodes: Nodes, state_graph: StateGraph):
        self.nodes = nodes
        self.workflow_app = state_graph
        self.app: CompiledStateGraph

        self._compile_workflow()

    @staticmethod
    def should_retry(state: MemoState) -> str:
        if not state.get("validation_errors"):
            return "done"
        if state.get("retry_count", 0) < MAX_RETRIES:
            return "retry"
        return "give_up"

    def _compile_workflow(self):
        self.workflow_app.add_node("merge_inputs",     self.nodes.merge_inputs)
        self.workflow_app.add_node("extract_entities", self.nodes.extract_entities)
        self.workflow_app.add_node("normalize_data",   self.nodes.normalize_data)
        self.workflow_app.add_node("budget_agent",     self.nodes.budget_agent)
        self.workflow_app.add_node("income_agent",     self.nodes.income_agent)
        self.workflow_app.add_node("risk_agent",       self.nodes.risk_agent)
        self.workflow_app.add_node("build_memo",       self.nodes.build_memo)
        self.workflow_app.add_node("build_memo_docx",    self.nodes.build_memo_docx)
        self.workflow_app.add_node("mark_as_failed",    self.nodes.mark_as_failed)

        self.workflow_app.set_entry_point("merge_inputs")
        self.workflow_app.add_edge("merge_inputs",     "extract_entities")
        self.workflow_app.add_edge("extract_entities", "normalize_data")

        self.workflow_app.add_edge("normalize_data",   "budget_agent")
        self.workflow_app.add_edge("normalize_data",   "income_agent")
        self.workflow_app.add_edge("normalize_data",   "risk_agent")

        self.workflow_app.add_edge("budget_agent",     "build_memo")
        self.workflow_app.add_edge("income_agent",     "build_memo")
        self.workflow_app.add_edge("risk_agent",       "build_memo")

        self.workflow_app.add_edge("build_memo",       "build_memo_docx")

        self.workflow_app.add_conditional_edges(
            "build_memo_docx",
            WorkFlow.should_retry,
            {
                "done":    END,
                "retry":   "budget_agent",
                "give_up": "mark_as_failed",
            },
        )

        self.workflow_app.add_edge("mark_as_failed", END)

        self.app = self.workflow_app.compile()