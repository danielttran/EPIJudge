"""Readonly rewindable integer stream; input ranges are private fixture storage."""
from models08 import TYPES
NUMBER_FILE={
'csharp':'public abstract class NumberFile { public abstract int ReadNext(); public abstract void Reset(); }\n',
'java':'abstract class NumberFile { public abstract int ReadNext(); public abstract void Reset(); }\n',
'cpp':'class NumberFile { public: virtual int ReadNext()=0; virtual void Reset()=0; virtual ~NumberFile()=default; };\n',
'python':'class NumberFile:\n    def ReadNext(self) -> int:\n        raise RuntimeError("Provided by the judge")\n    def Reset(self) -> None:\n        raise RuntimeError("Provided by the judge")\n',
'javascript':'class NumberFile {ReadNext(){throw new Error("Provided by the judge");}Reset(){throw new Error("Provided by the judge");}}\n'}
for language in TYPES:TYPES[language]['file']='NumberFile&' if language=='cpp' else 'NumberFile'
