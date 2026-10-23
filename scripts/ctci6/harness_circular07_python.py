"""Actual Python iterators, generic primitive values and expected range errors."""
CORE=r'''
def executeCircular7(row):
    kind,initial,operations,operands,new_values=row['arguments'];initial=initial.copy();saved=initial.copy();n=len(initial)
    def check(ok,message):
        if not ok:raise ValueError(message)
    def project(value):
        check(type(value) is (int if kind=='number' else str),'Preserve the selected generic element type')
        return value
    actor=CircularArray(initial)
    def read_iterator(iterator):
        result=[]
        for _ in range(n+1):
            try:result.append(project(next(iterator)))
            except StopIteration:break
        check(len(result)==n,'Iterators yield exactly the fixed number of elements')
        try:next(iterator)
        except StopIteration:return result
        raise ValueError('An exhausted iterator must remain exhausted')
    def snapshot():return read_iterator(iter(actor))
    def twice():
        first,second=iter(actor),iter(actor);left=[];right=[]
        for _ in range(n):left.append(project(next(first)));right.append(project(next(second)))
        for iterator in (first,second):
            try:next(iterator)
            except StopIteration:continue
            raise ValueError('Each independent iterator must finish after the fixed length')
        return [left,right]
    snapshot();check(initial==saved,'Copy caller sequence storage before later updates');results=[None]
    for operation,operand,value in zip(operations[1:],operands[1:],new_values[1:]):
        invalid=operation in ('Get','Set') and not 0<=operand<n
        before=snapshot() if invalid else None
        try:
            if operation=='Get':result=project(actor.Get(operand))
            elif operation=='Set':check(actor.Set(operand,value) is None,'Set returns None');result=None
            elif operation=='Rotate':check(actor.Rotate(operand) is None,'Rotate returns None');result=None
            elif operation=='Iterate':result=snapshot()
            elif operation=='IterateTwice':result=twice()
            else:raise ValueError('Unknown operation')
        except IndexError:
            if not invalid:raise
            check(snapshot()==before,'Invalid indexing must preserve state');result={'error':'index'}
        else:check(not invalid,'Invalid indexing must raise IndexError')
        check(initial==saved,'Preserve caller initial values during every update')
        results.append(result)
    return dict(actual=dict(results=results,finalValues=snapshot()),mutationOk=True)
'''
