"""Existing primitive/array bindings for the initial graph batch."""
from models08 import declare,header
from core import starter_body

def neutral(spec,language):
    if spec['result']=='ai':
        return 'return new int[0];' if language=='java' else 'return []' if language=='python' else 'return [];' if language in ('csharp','javascript') else 'return {};'
    return starter_body(spec,language)
