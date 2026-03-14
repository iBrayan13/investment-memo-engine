from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from src.langg.nodes import Nodes

class WorkFlow:
    def __init__(self, nodes: Nodes, state_graph: StateGraph):
        self.nodes = nodes
        self.workflow_app = state_graph
        self.app: CompiledStateGraph

        self._compile_workflow()

    def _compile_workflow(self):
        self.workflow_app.add_node("merge_inputs", self.nodes.merge_inputs)
        self.workflow_app.add_node("extract_entities", self.nodes.extract_entities)
        self.workflow_app.add_node("normalize_data", self.nodes.normalize_data)
        self.workflow_app.add_node("financial_agent", self.nodes.financial_agent)
        self.workflow_app.add_node("risk_agent", self.nodes.risk_agent)
        self.workflow_app.add_node("build_memo", self.nodes.build_memo)
        self.workflow_app.add_node("validate_json", self.nodes.validate_json)

        self.workflow_app.set_entry_point("merge_inputs")

        self.workflow_app.add_edge("merge_inputs", "extract_entities")
        self.workflow_app.add_edge("extract_entities", "normalize_data")
        self.workflow_app.add_edge("normalize_data", "financial_agent")
        self.workflow_app.add_edge("financial_agent", "risk_agent")
        self.workflow_app.add_edge("risk_agent", "build_memo")
        self.workflow_app.add_edge("build_memo", "validate_json")

        self.workflow_app.add_edge("validate_json", END)

        self.app = self.workflow_app.compile()