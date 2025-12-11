GRAPH = {
    'nodes': {
        'start': {
            'name': 'start',
            'func_name': 'extract_functions',
            'params': {}
        },
        'complexity': {
            'name': 'complexity',
            'func_name': 'check_complexity',
            'params': {}
        },
        'detect': {
            'name': 'detect',
            'func_name': 'detect_issues',
            'params': {}
        },
        'suggest': {
            'name': 'suggest',
            'func_name': 'suggest_improvements',
            'params': {'threshold': 85}
        }
    },
    'edges': {
        'start': 'complexity',
        'complexity': 'detect',
        'detect': {
            "state.get('quality_score',0) >= 85": 'suggest',
            'else': 'detect'
        }
    }
}
