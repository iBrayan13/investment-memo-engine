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

        self.app = self.workflow_app.compile()