"""Only an independent uniform 0..4 primitive is supplied to the solution."""
from models08 import TYPES
RAND5={
'csharp':'public abstract class Rand5Source { public abstract int Next(); }\n',
'java':'abstract class Rand5Source { public abstract int Next(); }\n',
'cpp':'class Rand5Source { public: virtual int Next()=0; virtual ~Rand5Source()=default; };\n',
'python':'class Rand5Source:\n    def Next(self) -> int:\n        raise RuntimeError("Provided by the judge")\n',
'javascript':'class Rand5Source {Next(){throw new Error("Provided by the judge");}}\n'}
for language in TYPES:TYPES[language]['rand5']='Rand5Source&' if language=='cpp' else 'Rand5Source'
