"""Bank-supplied uniform inclusive index primitive, shared with existing practice."""
from models08 import TYPES
for language,kind in [('csharp','void'),('java','void'),('cpp','void'),('python','None')]:TYPES[language]['v']=kind
RANDOM={
'csharp':'public static class RandomSource { internal static Func<int,int,int> Draw=(lower,upper)=>throw new InvalidOperationException("Provided by the judge"); public static int GetRandom(int lower,int upper)=>Draw(lower,upper); }\n',
'java':'class RandomSource { static java.util.function.IntBinaryOperator Draw=(lower,upper)->{throw new IllegalStateException("Provided by the judge");}; public static int GetRandom(int lower,int upper){return Draw.applyAsInt(lower,upper);} }\n',
'cpp':'#include <stdexcept>\nstruct RandomSource { inline static std::function<int(int,int)> Draw=[](int,int)->int{throw std::runtime_error("Provided by the judge");}; static int GetRandom(int lower,int upper){return Draw(lower,upper);} };\n',
'python':'class RandomSource:\n    @staticmethod\n    def GetRandom(lower: int,upper: int) -> int:\n        return RandomSource.Draw(lower,upper)\n',
'javascript':'class RandomSource {static Draw=(lower,upper)=>{throw new Error("Provided by the judge");};static GetRandom(lower,upper){return RandomSource.Draw(lower,upper);}}\n'}
REFERENCE={
'csharp':'public static class RandomSource { public static int GetRandom(int lower,int upper){throw new System.InvalidOperationException("Provided by the judge");} }\n',
'java':'class RandomSource { public static int GetRandom(int lower,int upper){throw new IllegalStateException("Provided by the judge");} }\n',
'cpp':'struct RandomSource { static int GetRandom(int lower,int upper); };\n',
'python':'class RandomSource:\n    @staticmethod\n    def GetRandom(lower: int,upper: int) -> int:\n        raise RuntimeError("Provided by the judge")\n',
'javascript':'class RandomSource {static GetRandom(lower,upper){throw new Error("Provided by the judge");}}\n'}
