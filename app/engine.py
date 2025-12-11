from typing import Any, Callable, Dict, Optional, List
import asyncio
import uuid
from pydantic import BaseModel

class NodeDef(BaseModel):
    name: str
    func_name: str
    params: Optional[Dict[str, Any]] = {}
    condition: Optional[str] = None

class GraphDef(BaseModel):
    nodes: Dict[str, NodeDef]
    edges: Dict[str, Any]

class RunState(BaseModel):
    run_id: str
    graph_id: str
    current_node: Optional[str] = None
    state: Dict[str, Any] = {}
    log: List[str] = []
    finished: bool = False

class GraphEngine:
    def __init__(self):
        self.graphs: Dict[str, GraphDef] = {}
        self.runs: Dict[str, RunState] = {}
        self.tools: Dict[str, Callable] = {}

    def register_tool(self, name: str, fn: Callable):
        self.tools[name] = fn

    def create_graph(self, graph_def: Dict) -> str:
        graph_id = str(uuid.uuid4())
        gd = GraphDef(**graph_def)
        self.graphs[graph_id] = gd
        return graph_id

    async def run_graph(self, graph_id: str, initial_state: Dict[str, Any]) -> str:
        run_id = str(uuid.uuid4())
        run = RunState(run_id=run_id, graph_id=graph_id, state=initial_state)
        self.runs[run_id] = run
        asyncio.create_task(self._execute_run(run_id))
        return run_id

    async def _execute_run(self, run_id: str):
        run = self.runs[run_id]
        graph = self.graphs[run.graph_id]
        start = 'start'
        node_name = start

        while node_name and not run.finished:
            run.current_node = node_name
            node_def = graph.nodes[node_name]
            await self._execute_node(node_def, run)
            node_name = self._get_next_node(node_def, graph, run)
            await asyncio.sleep(0)

        run.finished = True
        run.current_node = None

    async def _execute_node(self, node_def: NodeDef, run: RunState):
        fn = self.tools.get(node_def.func_name)
        result = fn(run.state, **(node_def.params or {}))
        if asyncio.iscoroutine(result):
            result = await result
        if isinstance(result, dict):
            run.state.update(result)

    def _get_next_node(self, node_def: NodeDef, graph: GraphDef, run: RunState):
        edges = graph.edges.get(node_def.name)
        if isinstance(edges, str):
            return edges
        if isinstance(edges, dict):
            for cond, target in edges.items():
                if cond == "else":
                    continue
                if eval(cond, {"state": run.state}):
                    return target
            return edges.get("else")
        return None

    def get_run(self, run_id: str) -> RunState:
        return self.runs[run_id]
