"""Actual stable resource-lock identities; serialized factory calls and native clients."""
CORE=r'''
def execute(row):
    import threading,time
    count,declarations,requests,_=row['arguments'];gates=[threading.Semaphore(1) for _ in range(count)]
    mutex=threading.Lock();local=threading.local();owners=[-1]*count;errors=[];plans=[[] for _ in range(4)];first_forks=[None]*4;first_acquired=[False]*4;phase=threading.Event();eligible=[False]*4
    def check_phase():
        if all(not eligible[r] or first_forks[r] is not None and (first_acquired[r] or owners[first_forks[r]]!=-1) for r in range(4)):phase.set()
    class Lock(ResourceLock):
        def __init__(self,resource):self.resource=resource
        def Lock(self):
            role=getattr(local,'role',-1)
            if not 0<=role<4:raise RuntimeError('Acquire locks only in registered native clients')
            with mutex:
                first=first_forks[role] is None
                if first:first_forks[role]=self.resource
                check_phase()
            if not gates[self.resource].acquire(timeout=1):raise RuntimeError('Granted lock orders deadlocked')
            with mutex:
                if owners[self.resource]!=-1:raise RuntimeError('Resource lock was not exclusive')
                owners[self.resource]=role
                if first:first_acquired[role]=True
                check_phase()
            if first and not phase.wait(1):raise RuntimeError('Initial acquisition schedule did not complete')
        def Unlock(self):
            role=getattr(local,'role',-1)
            with mutex:
                if role<0 or owners[self.resource]!=role:raise RuntimeError('Release only held native locks')
                owners[self.resource]=-1
            gates[self.resource].release()
    locks=[Lock(r) for r in range(count)]
    class Pool(LockPool):
        def Get(self,resource):
            if type(resource) is not int or not 0<=resource<count:raise RuntimeError('Invalid pool resource')
            return locks[resource]
    pool=Pool();factory=DeadlockFreeLocks(count,pool);admitted=[];grants=[];valid=True
    for declaration in declarations:
        owner=declaration[0];order=declaration[1:];before=order.copy();decision=factory.Declare(owner,order)
        if type(decision) is not bool:raise RuntimeError('Declare must return bool')
        admitted.append(decision);valid &= order==before
        for i in range(len(order)):order[i]=-999
    other=DeadlockFreeLocks(count,pool)
    for owner in range(4):
        for resource in range(count):valid &= other.GetLock(owner,resource) is None
    for owner,resource in requests:
        granted=factory.GetLock(owner,resource);grants.append(granted is not None)
        if granted is not None:
            if not 0<=owner<4 or not 0<=resource<count or granted is not locks[resource]:valid=False
            else:plans[owner].append(granted)
    if valid and any(plans):
        eligible[:]=[bool(plan) for plan in plans];ready=threading.Barrier(5,timeout=1)
        def client(role):
            acquired=[]
            try:
                local.role=role;ready.wait()
                for lock in plans[role]:lock.Lock();acquired.append(lock)
                time.sleep(.002)
            except BaseException as error:
                with mutex:errors.append(str(error))
            finally:
                for lock in reversed(acquired):
                    try:lock.Unlock()
                    except BaseException as error:
                        with mutex:errors.append(str(error))
                local.role=-1
        threads=[threading.Thread(target=client,args=(role,),daemon=True) for role in range(4)]
        for thread in threads:thread.start()
        try:ready.wait()
        except threading.BrokenBarrierError:errors.append('Clients did not become ready')
        for thread in threads:thread.join(1.5)
        valid &= not errors and all(not t.is_alive() for t in threads) and all(owner==-1 for owner in owners)
    return dict(actual=dict(declarations=admitted,grants=grants),mutationOk=bool(valid))
'''
