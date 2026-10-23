"""Four real workers pass one permit to the role responsible for the next item."""
def body(language):
 if language=='python':return '''def owner(value):
    return 3 if value%15==0 else 1 if value%3==0 else 2 if value%5==0 else 0
for value in range(1,limit+1):
    if owner(value)!=role:continue
    context.Wait(role)
    context.Print(value)
    if value<limit:context.Signal(owner(value+1))'''
 if language=='javascript':return '''const owner=value=>value%15===0?3:value%3===0?1:value%5===0?2:0;
for(let value=1;value<=limit;++value){if(owner(value)!==role)continue;context.Wait(role);context.Print(value);if(value<limit)context.Signal(owner(value+1));}'''
 if language=='cpp':return '''auto owner=[](int value){return value%15==0?3:value%3==0?1:value%5==0?2:0;};
for(int value=1;value<=limit;++value){if(owner(value)!=role)continue;context.Wait(role);context.Print(value);if(value<limit)context.Signal(owner(value+1));}'''
 if language=='csharp':return '''int Owner(int value)=>value%15==0?3:value%3==0?1:value%5==0?2:0;
for(int value=1;value<=limit;++value){if(Owner(value)!=role)continue;context.Wait(role);context.Print(value);if(value<limit)context.Signal(Owner(value+1));}'''
 return '''java.util.function.IntUnaryOperator owner=value->value%15==0?3:value%3==0?1:value%5==0?2:0;
for(int value=1;value<=limit;++value){if(owner.applyAsInt(value)!=role)continue;context.Wait(role);context.Print(value);if(value<limit)context.Signal(owner.applyAsInt(value+1));}'''
