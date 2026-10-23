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
def reference(ref,language):
    if ref=='15.4':
        from models_locks15 import API as LOCK_API
        return LOCK_API[language]
    if ref=='15.3':
        from models_dining15 import API as FORK_API
        return FORK_API[language]
    if ref=='15.7':
        from models_fizz15 import API as FIZZ_API
        return FIZZ_API[language]
    return API[language]
def names(ref):return ['ResourceLock','LockPool'] if ref=='15.4' else ['ForkContext'] if ref=='15.3' else ['FizzContext'] if ref=='15.7' else ['SyncContext']
def header(ref,language):return base_header(ref,language)+reference(ref,language)
def declare(spec,language,body,class_name='Solution'):
    if spec['ref']=='15.4':
        from models_locks15 import SIGNATURE
        return SIGNATURE[language],body
    from core import declaration
    contract=dict(spec,params=([('role','i'),('philosophers','i'),('bites','i'),('context','forksync')] if spec['ref']=='15.3' else [('role','i'),('limit','i'),('context','fizzsync')] if spec['ref']=='15.7' else [('role','i'),('context','sync')]),result='void')
    from core import TYPES
    for lang in ('csharp','java','cpp','python'):TYPES[lang]['sync']={'csharp':'SyncContext','java':'SyncContext','cpp':'SyncContext&','python':'SyncContext'}[lang]
    for lang in ('csharp','java','cpp','python'):TYPES[lang]['fizzsync']={'csharp':'FizzContext','java':'FizzContext','cpp':'FizzContext&','python':'FizzContext'}[lang]
    for lang in ('csharp','java','cpp','python'):TYPES[lang]['forksync']={'csharp':'ForkContext','java':'ForkContext','cpp':'ForkContext&','python':'ForkContext'}[lang]
    return declaration(contract,language,body,class_name)
def neutral(spec,language):
    if spec['ref']=='15.4':
        from models_locks15 import neutral as run
        return run(language)
    return 'return' if language=='python' else 'return;'
