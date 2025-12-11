from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn
from app.engine import GraphEngine
from app import tools
from app.workflows import code_review

app = FastAPI(title='Minimal Workflow Engine')
engine = GraphEngine()

# register tools
engine.register_tool('extract_functions', tools.extract_functions)
engine.register_tool('check_complexity', tools.check_complexity)
engine.register_tool('detect_issues', tools.detect_issues)
engine.register_tool('suggest_improvements', tools.suggest_improvements)
engine.register_tool('long_running_check', tools.long_running_check)

class CreateGraphIn(BaseModel):
    graph: Dict[str, Any]

class RunGraphIn(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any]

@app.post('/graph/create')
async def create_graph(payload: CreateGraphIn):
    try:
        graph_id = engine.create_graph(payload.graph)
        return {'graph_id': graph_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post('/graph/run')
async def run_graph(payload: RunGraphIn):
    try:
        run_id = await engine.run_graph(payload.graph_id, payload.initial_state)
        return {'run_id': run_id}
    except KeyError:
        raise HTTPException(status_code=404, detail='graph not found')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/graph/state/{run_id}')
async def get_state(run_id: str):
    try:
        run = engine.get_run(run_id)
        return {'run_id': run.run_id, 'state': run.state, 'log': run.log, 'finished': run.finished}
    except KeyError:
        raise HTTPException(status_code=404, detail='run not found')

@app.post('/graph/create/sample/code_review')
async def create_sample():
    gid = engine.create_graph(code_review.GRAPH)
    return {'graph_id': gid}

if __name__ == '__main__':
    uvicorn.run('app.main:app', host='0.0.0.0', port=8000, reload=True)
