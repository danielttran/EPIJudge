"""Observe ordered subsets and lift duplicate-valued outputs to uniform masks."""
CORE=r'''
class SubsetState13:
    Input=[]
    LastOutput=[]
    @staticmethod
    def check(ok,message):
        if not ok:raise ValueError(message)
    class Coins(FairCoinSource):
        def __init__(self,source):self.source=source;self.calls=0
        def Next(self):
            self.calls+=1
            SubsetState13.check(self.calls<=64*len(SubsetState13.Input)+128,'Subset exceeded the supplied-coin budget')
            return self.source.Next()==1
    @staticmethod
    def sample(source):
        values=SubsetState13.Input.copy();result=RandomSubset(values,SubsetState13.Coins(source))
        SubsetState13.check(values==SubsetState13.Input,'Preserve input values and order')
        SubsetState13.check(type(result) is list and all(type(v) is int for v in result),'Return a concrete integer subset')
        cursor=0
        for value in result:
            while cursor<len(values) and values[cursor]!=value:cursor+=1
            SubsetState13.check(cursor<len(values),'Return an ordered subsequence of original occurrences')
            cursor+=1
        SubsetState13.LastOutput=result.copy()
        return result
    @staticmethod
    def mask(source):
        result=SubsetState13.sample(source);values=SubsetState13.Input;n=len(values);m=len(result)
        ways=[[0]*(m+1) for _ in range(n+1)]
        for i in range(n+1):ways[i][m]=1
        for i in range(n-1,-1,-1):
            for j in range(m-1,-1,-1):ways[i][j]=ways[i+1][j]+(ways[i+1][j+1] if values[i]==result[j] else 0)
        mask=j=0
        for i in range(n):
            choose=ways[i+1][j+1] if j<m and values[i]==result[j] else 0
            total=ways[i][j]
            ticket=0
            if total>1:
                bits=(total-1).bit_length()
                while True:
                    ticket=0
                    for _ in range(bits):ticket=(ticket<<1)|source.Next()
                    if ticket<total:break
            if ticket<choose:mask|=1<<i;j+=1
        return mask
    @staticmethod
    def large():
        values=SubsetState13.Input;n=len(values);samples=128 if n>64 else 4096
        class SeedBits(ChoiceBitSource):
            def __init__(self):self.seed=0x85ebca6b
            def Next(self):self.seed=(self.seed*1664525+1013904223)&0xffffffff;return self.seed>>31
        source=SeedBits();totals={value:0 for value in values};multiplicities={value:values.count(value) for value in totals};length_sum=squares=0
        for _ in range(samples):
            result=SubsetState13.sample(source);length_sum+=len(result);squares+=(len(result)-n/2)**2
            for value in result:totals[value]+=1
        statistic=sum((totals[v]-samples*m/2)**2/(samples*m/4) for v,m in multiplicities.items())
        SubsetState13.check(statistic<4*len(totals)+80,'Subset inclusion frequencies are biased')
        SubsetState13.check((length_sum-samples*n/2)**2/(samples*n/4)<40,'Subset sizes are biased')
        SubsetState13.check(0.25<squares/(samples*n/4)<4,'Subset size variation must reflect independent choices')
        return dict(actual=SubsetState13.LastOutput,mutationOk=True,uniformOk=True)
def ChooseMask13(source):return SubsetState13.mask(source)
'''

def finish(value):
    value=value.replace('def executeSubset13(row):','def executeSubset13(row):\n    SubsetState13.Input=row["arguments"][0].copy()\n    if len(SubsetState13.Input)>5:return SubsetState13.large()')
    value=value.replace("random_check([[value+1 for value in row['arguments'][0]]])","random_check([[]])")
    return value.replace("actual=context['first']",'actual=SubsetState13.LastOutput')
