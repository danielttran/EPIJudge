"""Real fork semaphores and ownership observations across native Python threads."""
CORE=r'''
def execute(row):
    import threading,time
    n,bites,order,mask,_=row['arguments'];gates=[threading.Semaphore(1) for _ in range(n)]
    ready=threading.Barrier(n+1,timeout=1);lock=threading.Lock();owners=[-1]*n;meals=[0]*n;events=[];errors=[];first_forks=[None]*n;first_acquired=[False]*n;phase=threading.Event()
    def check_phase():
        if all(first_forks[r] is not None and (first_acquired[r] or owners[first_forks[r]]!=-1) for r in range(n)):phase.set()
    class Context(ForkContext):
        def __init__(self,role):self.role=role;self.owner=threading.get_ident();self.calls=0
        def check(self,fork=None):
            self.calls+=1
            if threading.get_ident()!=self.owner or self.calls>10000*(bites+1) or fork is not None and (type(fork) is not int or fork not in (self.role,(self.role+1)%n)):raise RuntimeError('Use only owned worker and adjacent fork API')
        def Take(self,fork):
            self.check(fork)
            with lock:
                first=first_forks[self.role] is None
                if first:first_forks[self.role]=fork
                check_phase()
            if not gates[fork].acquire(timeout=1):raise RuntimeError('Fork acquisition did not complete')
            with lock:
                if owners[fork]!=-1:raise RuntimeError('Fork lock was not exclusive')
                owners[fork]=self.role
                if first:first_acquired[self.role]=True
                check_phase()
            if first and not phase.wait(1):raise RuntimeError('Initial acquisition schedule did not complete')
        def Drop(self,fork):
            self.check(fork)
            with lock:
                if owners[fork]!=self.role:raise RuntimeError('Release only a held fork')
                owners[fork]=-1
            gates[fork].release()
        def Eat(self):
            self.check()
            with lock:
                if owners[self.role]!=self.role or owners[(self.role+1)%n]!=self.role or meals[self.role]>=bites:raise RuntimeError('Eat exactly the requested bites while holding both adjacent forks')
                meals[self.role]+=1;events.append(self.role)
            time.sleep(.002)
    def worker(role):
        try:
            context=Context(role);ready.wait()
            if mask>>role&1:time.sleep(.004)
            if Dine(role,n,bites,context) is not None:raise RuntimeError('Dine must return None')
        except BaseException as error:
            with lock:errors.append(str(error))
    threads=[threading.Thread(target=worker,args=(role,),daemon=True) for role in order]
    for thread in threads:thread.start()
    try:ready.wait()
    except threading.BrokenBarrierError:errors.append('Workers did not become ready')
    for thread in threads:thread.join(1.5)
    return dict(actual=events,mutationOk=not errors and all(v==bites for v in meals) and all(v==-1 for v in owners) and all(not t.is_alive() for t in threads))
'''
