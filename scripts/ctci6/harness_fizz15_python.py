"""Four real threads print through an opaque role-bound callback."""
CORE=r'''
def execute(row):
    import threading,time
    limit,order,mask,_=row['arguments'];gates=[threading.Semaphore(int(i==0)) for i in range(4)]
    ready=threading.Barrier(5,timeout=1);lock=threading.Lock();events=[];errors=[];next_value=1;printing=False
    def owner(v):return 3 if v%15==0 else 1 if v%3==0 else 2 if v%5==0 else 0
    class Context(FizzContext):
        def __init__(self,role):self.role=role;self.owner=threading.get_ident();self.calls=0
        def check(self,gate=None):
            self.calls+=1
            if threading.get_ident()!=self.owner or self.calls>4*(limit+1) or gate is not None and (type(gate) is not int or not 0<=gate<4):raise RuntimeError('Invalid synchronization API call')
        def Wait(self,gate):
            self.check(gate)
            if not gates[gate].acquire(timeout=1):raise RuntimeError('Synchronization did not complete')
        def Signal(self,gate):self.check(gate);gates[gate].release()
        def Print(self,value):
            nonlocal next_value,printing
            self.check()
            with lock:
                if type(value) is not int or not 1<=value<=limit or value!=next_value or printing or owner(value)!=self.role:raise RuntimeError('Wrong printing role, duplicate, overlap or out-of-order item')
                printing=True
            time.sleep(.002)
            with lock:
                events.append(('Fizz' if value%3==0 else '')+('Buzz' if value%5==0 else '') or str(value));next_value+=1;printing=False
    def worker(role):
        try:
            context=Context(role);ready.wait()
            if mask>>role&1:time.sleep(.004)
            if RunFizzBuzz(role,limit,context) is not None:raise RuntimeError('RunFizzBuzz must return None')
        except BaseException as error:
            with lock:errors.append(str(error))
    threads=[threading.Thread(target=worker,args=(role,),daemon=True) for role in order]
    for thread in threads:thread.start()
    try:ready.wait()
    except threading.BrokenBarrierError:errors.append('Workers did not become ready')
    for thread in threads:thread.join(1.5)
    return dict(actual=events,mutationOk=not errors and next_value==limit+1 and not printing and all(not t.is_alive() for t in threads))
'''
