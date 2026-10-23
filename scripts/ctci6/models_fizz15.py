"""Opaque counting gates and role-bound actual printing callback."""
API={
'csharp':'public abstract class FizzContext {public abstract void Wait(int gate);public abstract void Signal(int gate);public abstract void Print(int value);}\n',
'java':'abstract class FizzContext {public abstract void Wait(int gate);public abstract void Signal(int gate);public abstract void Print(int value);}\n',
'cpp':'class FizzContext {public:virtual void Wait(int gate)=0;virtual void Signal(int gate)=0;virtual void Print(int value)=0;protected:virtual ~FizzContext()=default;};\n',
'python':'''class FizzContext:
    def Wait(self,gate: int) -> None:
        raise RuntimeError("Provided synchronization primitive")
    def Signal(self,gate: int) -> None:
        raise RuntimeError("Provided synchronization primitive")
    def Print(self,value: int) -> None:
        raise RuntimeError("Provided role-bound print callback")
''',
'javascript':'''class FizzContext {Wait(gate){throw new Error('Provided synchronization primitive');}Signal(gate){throw new Error('Provided synchronization primitive');}Print(value){throw new Error('Provided role-bound print callback');}}\n'''}
