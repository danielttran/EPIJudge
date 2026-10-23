"""Independent semaphore handoff, with no timing or launch-order assumptions."""
def body(ref,language):
    if ref!='15.5':raise ValueError(ref)
    if language=='python':return '''if role>0:
    context.Wait(role-1)
context.Work()
if role<2:
    context.Signal(role)'''
    op='->' if language=='cpp' else '.'
    if language=='cpp':op='.'
    return 'if(role>0)context'+op+'Wait(role-1);\ncontext'+op+'Work();\nif(role<2)context'+op+'Signal(role);'

_order_body=body
def body(ref,language):
    if ref=='15.7':
        from algorithms_fizz15 import body as run
        return run(language)
    return _order_body(ref,language)

_fizz_body=body
def body(ref,language):
    if ref=='15.3':
        from algorithms_dining15 import body as run
        return run(language)
    return _fizz_body(ref,language)

_dining_body=body
def body(ref,language):
    if ref=='15.4':
        from algorithms_locks15 import body as run
        return run(language)
    return _dining_body(ref,language)
