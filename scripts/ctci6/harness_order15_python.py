"""Real threading workers and opaque native semaphore callbacks."""
CORE=r'''
def execute(row):
    import threading,time
    order,mask,_=row['arguments']
    gates=[threading.Semaphore(0),threading.Semaphore(0)]
    ready=threading.Barrier(4,timeout=1)
    lock=threading.Lock();events=[];completed=[False]*3;invoked=[False]*3;errors=[]
    class Context(SyncContext):
        def __init__(self,role):self.role=role;self.owner=threading.get_ident();self.calls=0
        def check(self,gate=None):
            self.calls+=1
            if threading.get_ident()!=self.owner or self.calls>20 or gate is not None and (type(gate) is not int or gate not in (0,1)):raise RuntimeError('Invalid synchronization API call')
        def Wait(self,gate):
            self.check(gate)
            if not gates[gate].acquire(timeout=1):raise RuntimeError('Synchronization did not complete')
        def Signal(self,gate):self.check(gate);gates[gate].release()
        def Work(self):
            self.check()
            with lock:
                if invoked[self.role] or self.role and not completed[self.role-1]:raise RuntimeError('Work started before predecessor completion or ran twice')
                invoked[self.role]=True;events.append(self.role)
            time.sleep(.002)
            with lock:completed[self.role]=True
    def worker(role):
        try:
            context=Context(role);ready.wait()
            if mask>>role&1:time.sleep(.004)
            result=RunOrdered(role,context)
            if result is not None:raise RuntimeError('RunOrdered must return None')
        except BaseException as error:
            with lock:errors.append(str(error))
    threads=[threading.Thread(target=worker,args=(role,),daemon=True) for role in order]
    for thread in threads:thread.start()
    try:ready.wait()
    except threading.BrokenBarrierError:errors.append('Workers did not become ready')
    for thread in threads:thread.join(1.5)
    return dict(actual=events,mutationOk=not errors and all(completed) and all(not t.is_alive() for t in threads))
'''
