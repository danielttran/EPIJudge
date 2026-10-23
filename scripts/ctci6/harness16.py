"""Reuse the typed, expected-answer-free submission adapter."""
from harness08_typed import source as typed_source
from models08 import header as base_header
from models16 import header

def source(language,starters=False,only_ref=None):
    value=typed_source(language,starters,only_ref,staging_name='staged16')
    if language=='python':value=value.replace('else type(actual) is int and -2147483648<=actual<=2147483647', "else type(actual) is int and -1<=actual<=4294967295 if kind=='l' else type(actual) is int and -2147483648<=actual<=2147483647")
    if language=='javascript':value=value.replace(':Number.isInteger(actual)&&actual>=-2147483648&&actual<=2147483647;', ":kind==='l'?Number.isSafeInteger(actual)&&actual>=-1&&actual<=4294967295:Number.isInteger(actual)&&actual>=-2147483648&&actual<=2147483647;")
    if language=='cpp':
        ref=only_ref or '8.4'
        value=value.replace(base_header(ref,language),header(ref,language),1)
    if language=='java':
        value=value.replace('if(value instanceof Integer v)return Json.value(v);','if(value instanceof Integer v)return Json.value(v);if(value instanceof Long v)return Json.value(v);')
    return value
