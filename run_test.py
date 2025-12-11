# Simple test runner for the assignment repo.
# It imports the engine and tools, creates a simple graph and ensures
# the graph runs to completion. Exit code 0 = success, nonzero = fail.

import asyncio
import sys
from app.engine import GraphEngine
from app import tools
from app.workflows import code_review

async def run_simple_test():
    engine = GraphEngine()
    # register tools — these names must match your app/tools.py
    engine.register_tool('extract_functions', tools.extract_functions)
    engine.register_tool('check_complexity', tools.check_complexity)
    engine.register_tool('detect_issues', tools.detect_issues)
    engine.register_tool('suggest_improvements', tools.suggest_improvements)
    engine.register_tool('long_running_check', tools.long_running_check)

    # We'll run a short simple graph that finishes quickly
    GRAPH_SIMPLE = {
        'nodes': {
            'start': {'name':'start', 'func_name':'extract_functions', 'params':{}},
            'suggest': {'name':'suggest', 'func_name':'suggest_improvements', 'params':{'threshold': 50}}
        },
        'edges': { 'start': 'suggest' }
    }

    gid = engine.create_graph(GRAPH_SIMPLE)
    run_id = await engine.run_graph(gid, {'code': 'def add(a,b):\\n    return a+b'})

    # wait for the run to finish (timeout after a few seconds)
    for _ in range(200):
        run = engine.get_run(run_id)
        if run.finished:
            break
        await asyncio.sleep(0.05)

    run = engine.get_run(run_id)
    # Basic assertions
    if not run.finished:
        print("ERROR: run did not finish", file=sys.stderr)
        print("LOG:", *run.log, sep="\n", file=sys.stderr)
        return 2
    # check that suggestions were produced
    if 'suggestions' not in run.state:
        print("ERROR: suggestions missing from final state", file=sys.stderr)
        print("FINAL STATE:", run.state, file=sys.stderr)
        return 3

    print("SUCCESS: test completed. Final state keys:", list(run.state.keys()))
    return 0

if __name__ == "__main__":
    rc = asyncio.get_event_loop().run_until_complete(run_simple_test())
    # propagate return code so GitHub Actions knows pass/fail
    sys.exit(rc)
