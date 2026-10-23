"""Break circular wait by globally ordering acquisition of adjacent fork locks."""
def body(language):
 if language=='python':return '''left,right=role,(role+1)%philosophers
lower,higher=min(left,right),max(left,right)
for _ in range(bites):
    context.Take(lower)
    context.Take(higher)
    context.Eat()
    context.Drop(higher)
    context.Drop(lower)'''
 if language=='javascript':return '''const left=role,right=(role+1)%philosophers,lower=Math.min(left,right),higher=Math.max(left,right);
for(let bite=0;bite<bites;++bite){context.Take(lower);context.Take(higher);context.Eat();context.Drop(higher);context.Drop(lower);}'''
 if language=='cpp':return '''int left=role,right=(role+1)%philosophers,lower=std::min(left,right),higher=std::max(left,right);
for(int bite=0;bite<bites;++bite){context.Take(lower);context.Take(higher);context.Eat();context.Drop(higher);context.Drop(lower);}'''
 if language=='csharp':return '''int left=role,right=(role+1)%philosophers,lower=Math.Min(left,right),higher=Math.Max(left,right);
for(int bite=0;bite<bites;++bite){context.Take(lower);context.Take(higher);context.Eat();context.Drop(higher);context.Drop(lower);}'''
 return '''int left=role,right=(role+1)%philosophers,lower=Math.min(left,right),higher=Math.max(left,right);
for(int bite=0;bite<bites;++bite){context.Take(lower);context.Take(higher);context.Eat();context.Drop(higher);context.Drop(lower);}'''
