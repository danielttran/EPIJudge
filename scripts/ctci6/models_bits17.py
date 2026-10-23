"""Only single-bit access is exposed for the missing-number exercise."""
from models08 import TYPES
BITS={
'csharp':'public abstract class BitArray { public abstract int Size(); public abstract int FetchBit(int index,int column); }\n',
'java':'abstract class BitArray { public abstract int Size(); public abstract int FetchBit(int index,int column); }\n',
'cpp':'class BitArray { public: virtual int Size()=0; virtual int FetchBit(int index,int column)=0; virtual ~BitArray()=default; };\n',
'python':'class BitArray:\n    def Size(self) -> int:\n        raise RuntimeError("Provided by the judge")\n    def FetchBit(self,index: int,column: int) -> int:\n        raise RuntimeError("Provided by the judge")\n',
'javascript':'class BitArray { Size(){throw new Error("Provided by the judge");} FetchBit(index,column){throw new Error("Provided by the judge");} }\n'}
for language in TYPES:TYPES[language]['bits']='BitArray&' if language=='cpp' else 'BitArray'
