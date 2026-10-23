"""Provided adjacent-fork lock and real eating callback API."""
API={
'csharp':'public abstract class ForkContext {public abstract void Take(int fork);public abstract void Drop(int fork);public abstract void Eat();}\n',
'java':'abstract class ForkContext {public abstract void Take(int fork);public abstract void Drop(int fork);public abstract void Eat();}\n',
'cpp':'class ForkContext {public:virtual void Take(int fork)=0;virtual void Drop(int fork)=0;virtual void Eat()=0;protected:virtual ~ForkContext()=default;};\n',
'python':'''class ForkContext:
    def Take(self,fork: int) -> None:
        raise RuntimeError("Provided fork lock")
    def Drop(self,fork: int) -> None:
        raise RuntimeError("Provided fork lock")
    def Eat(self) -> None:
        raise RuntimeError("Provided eating callback")
''',
'javascript':'''class ForkContext {Take(fork){throw new Error('Provided fork lock');}Drop(fork){throw new Error('Provided fork lock');}Eat(){throw new Error('Provided eating callback');}}\n'''}
