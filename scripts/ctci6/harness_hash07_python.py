"""Observe actual generic map calls; final entries are obtained only through Get."""
CORE=r'''
def executeHash7(row):
    kind,capacity,operations,keys,values=row['arguments'];text_keys=kind=='text-number'
    def check(ok,message):
        if not ok:raise ValueError(message)
    def key_copy(key):return key.encode('utf-8').decode('utf-8') if text_keys else int(str(key))
    def project(value):
        check(type(value) is (int if text_keys else str),'Preserve the selected generic value type')
        return value
    actor=HashTable(capacity);other=HashTable(capacity)
    check(other.Put(key_copy(keys[0]),values[0]) is None,'Put returns None')
    present=actor.Contains(key_copy(keys[0]));check(type(present) is bool and not present,'New table instances own independent empty state')
    results=[None];seen=[]
    for operation,key,value in zip(operations[1:],keys[1:],values[1:]):
        if key not in seen:seen.append(key)
        supplied=key_copy(key)
        if operation=='Put':check(actor.Put(supplied,value) is None,'Put returns None');result=None
        elif operation=='Get':
            try:result=project(actor.Get(supplied))
            except KeyError:result={'error':'missing'}
        elif operation=='Remove':result=actor.Remove(supplied);check(type(result) is bool,'Remove returns a boolean')
        elif operation=='Contains':result=actor.Contains(supplied);check(type(result) is bool,'Contains returns a boolean')
        else:raise ValueError('Unknown operation')
        results.append(result)
    entries=[]
    for key in seen:
        try:entries.append([key,project(actor.Get(key_copy(key)))])
        except KeyError:pass
    return dict(actual=dict(results=results,finalEntries=entries),mutationOk=True)
'''
