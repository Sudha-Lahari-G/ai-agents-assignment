import asyncio
from typing import Dict

def extract_functions(state: Dict, **kwargs):
    code = state.get('code', '')
    funcs = [s.split('\n',1)[0].strip() for s in code.split('def ')[1:]]
    return {'functions': funcs, 'quality_score': 0}

def check_complexity(state: Dict, **kwargs):
    funcs = state.get('functions', [])
    score = 100
    issues = 0
    for f in funcs:
        length = len(f)
        if length > 50:
            issues += 2
        elif length > 20:
            issues += 1
    qs = state.get('quality_score', 100) - issues*5
    return {'issues': issues, 'quality_score': max(qs, 0)}

def detect_issues(state: Dict, **kwargs):
    issues = state.get('issues', 0)
    found = issues + 1
    qs = state.get('quality_score', 100) - 10
    return {'issues': found, 'quality_score': max(qs, 0)}

def suggest_improvements(state: Dict, threshold: int = 80):
    qs = state.get('quality_score', 0)
    suggestions = []
    if qs < threshold:
        suggestions.append('Refactor large functions')
        suggestions.append('Add docstrings')
    else:
        suggestions.append('Looks good')
    return {'suggestions': suggestions}

async def long_running_check(state: Dict, delay: int = 1):
    await asyncio.sleep(delay)
    return {'long_check': 'done'}
