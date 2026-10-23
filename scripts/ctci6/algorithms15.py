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
