"""Opaque synchronization API; worker identity and work are owned by the judge."""
from models08 import header as base_header
API={
'csharp':'''public abstract class SyncContext {public abstract void Wait(int gate);public abstract void Signal(int gate);public abstract void Work();}\n''',
'java':'''abstract class SyncContext {public abstract void Wait(int gate);public abstract void Signal(int gate);public abstract void Work();}\n''',
'cpp':'''class SyncContext {public:virtual void Wait(int gate)=0;virtual void Signal(int gate)=0;virtual void Work()=0;protected:virtual ~SyncContext()=default;};\n''',
'python':'''class SyncContext:
    def Wait(self,gate: int) -> None:
        raise RuntimeError("Provided synchronization primitive")
    def Signal(self,gate: int) -> None:
        raise RuntimeError("Provided synchronization primitive")
    def Work(self) -> None:
        raise RuntimeError("Provided worker callback")
''',
'javascript':'''class SyncContext {Wait(gate){throw new Error('Provided synchronization primitive');}Signal(gate){throw new Error('Provided synchronization primitive');}Work(){throw new Error('Provided worker callback');}}\n'''}
def header(ref,language):return base_header(ref,language)+API[language]
def declare(spec,language,body,class_name='Solution'):
    from core import declaration
    contract=dict(spec,params=[('role','i'),('context','sync')],result='void')
    from core import TYPES
    for lang in ('csharp','java','cpp','python'):TYPES[lang]['sync']={'csharp':'SyncContext','java':'SyncContext','cpp':'SyncContext&','python':'SyncContext'}[lang]
    return declaration(contract,language,body,class_name)
def neutral(spec,language):return 'return' if language=='python' else 'return;'
