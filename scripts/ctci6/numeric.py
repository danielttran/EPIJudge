"""Finite real-valued result bindings; only selected numeric adapters change."""
from models08 import TYPES
for language,scalar,array in [('csharp','double','double[]'),('java','double','double[]'),('cpp','double','std::vector<double>'),('python','float','list[float]')]:
    TYPES[language].update(d=scalar,ad=array)

def adapt(value,language,kinds):
    if not kinds.intersection({'d','ad'}):return value
    if language=='python':
        value=value.replace('valid=(',"valid=(type(actual) in (int,float) and __import__('math').isfinite(actual)) if kind=='d' else (type(actual) is list and all(type(v) in (int,float) and __import__('math').isfinite(v) for v in actual)) if kind=='ad' else (",1)
    if language=='javascript':
        value=value.replace('const valid=',"const valid=kind==='d'?typeof actual==='number'&&Number.isFinite(actual):kind==='ad'?Array.isArray(actual)&&actual.every(v=>typeof v==='number'&&Number.isFinite(v)):",1)
    if language=='java':
        value=value.replace('if(value instanceof Integer v)return Json.value(v);','if(value instanceof Integer v)return Json.value(v);if(value instanceof Double v){if(!Double.isFinite(v))throw new IllegalArgumentException("Return finite numbers");return Json.value(v);}',1)
        value=value.replace('else if(value instanceof Iterable<?> values)','else if(value instanceof double[] values){for(double v:values){if(!Double.isFinite(v))throw new IllegalArgumentException("Return finite numbers");result.add(v);}}else if(value instanceof Iterable<?> values)',1)
    return value
