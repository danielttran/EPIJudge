"""Stable opaque native lock identities for the deadlock-preventing factory."""
API={
'csharp':'''public abstract class ResourceLock {public abstract void Lock();public abstract void Unlock();}
public abstract class LockPool {public abstract ResourceLock Get(int resource);}
''',
'java':'''abstract class ResourceLock {public abstract void Lock();public abstract void Unlock();}
abstract class LockPool {public abstract ResourceLock Get(int resource);}
''',
'cpp':'''class ResourceLock {public:virtual void Lock()=0;virtual void Unlock()=0;protected:virtual ~ResourceLock()=default;};
class LockPool {public:virtual ResourceLock* Get(int resource)=0;protected:virtual ~LockPool()=default;};
''',
'python':'''class ResourceLock:
    def Lock(self) -> None:
        raise RuntimeError("Provided native resource lock")
    def Unlock(self) -> None:
        raise RuntimeError("Provided native resource lock")
class LockPool:
    def Get(self,resource: int) -> ResourceLock:
        raise RuntimeError("Provided stable native lock pool")
''',
'javascript':'''class ResourceLock {Lock(){throw new Error('Provided native resource lock');}Unlock(){throw new Error('Provided native resource lock');}}
class LockPool {Get(resource){throw new Error('Provided stable native lock pool');}}
'''}
SIGNATURE={
'csharp':'DeadlockFreeLocks(int resourceCount,LockPool pool); bool Declare(int owner,int[] order); ResourceLock? GetLock(int owner,int resource)',
'java':'DeadlockFreeLocks(int resourceCount,LockPool pool); boolean Declare(int owner,int[] order); ResourceLock GetLock(int owner,int resource)',
'cpp':'DeadlockFreeLocks(int resourceCount,LockPool& pool); bool Declare(int owner,const std::vector<int>& order); ResourceLock* GetLock(int owner,int resource)',
'python':'DeadlockFreeLocks(resourceCount: int,pool: LockPool); Declare(owner: int,order: list[int]) -> bool; GetLock(owner: int,resource: int) -> ResourceLock | None',
'javascript':'new DeadlockFreeLocks(resourceCount,pool); Declare(owner,order); GetLock(owner,resource)'}
def neutral(language):return {
'csharp':'public class DeadlockFreeLocks {public DeadlockFreeLocks(int resourceCount,LockPool pool){}public bool Declare(int owner,int[] order)=>false;public ResourceLock? GetLock(int owner,int resource)=>null;}',
'java':'class DeadlockFreeLocks {public DeadlockFreeLocks(int resourceCount,LockPool pool){}public boolean Declare(int owner,int[] order){return false;}public ResourceLock GetLock(int owner,int resource){return null;}}',
'cpp':'class DeadlockFreeLocks {public:DeadlockFreeLocks(int resourceCount,LockPool& pool){}bool Declare(int owner,const std::vector<int>& order){return false;}ResourceLock* GetLock(int owner,int resource){return nullptr;}};',
'python':'class DeadlockFreeLocks:\n    def __init__(self,resourceCount: int,pool: LockPool):\n        self._unused=resourceCount\n    def Declare(self,owner: int,order: list[int]) -> bool:\n        return False\n    def GetLock(self,owner: int,resource: int) -> ResourceLock | None:\n        return None\n',
'javascript':'class DeadlockFreeLocks {constructor(resourceCount,pool){}Declare(owner,order){return false;}GetLock(owner,resource){return null;}}'}[language]
