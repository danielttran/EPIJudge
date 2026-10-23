"""Private ordered-subsequence observations and combinatorial duplicate lifting."""
CORE=r'''
class SubsetState13 {
static Input=[];static LastOutput=[];
static check(ok,message){if(!ok)throw Error(message);}
static Coins=class extends FairCoinSource{constructor(source){super();this.source=source;this.calls=0;}Next(){SubsetState13.check(++this.calls<=64*SubsetState13.Input.length+128,'Subset exceeded the supplied-coin budget');return this.source.Next()===1;}};
static sample(source){const values=this.Input.slice(),result=RandomSubset(values,new this.Coins(source));this.check(values.length===this.Input.length&&values.every((v,i)=>v===this.Input[i]),'Preserve input values and order');this.check(Array.isArray(result)&&result.every(Number.isInteger),'Return a concrete integer subset');let cursor=0;for(const value of result){while(cursor<values.length&&values[cursor]!==value)++cursor;this.check(cursor<values.length,'Return an ordered subsequence of original occurrences');++cursor;}this.LastOutput=result.slice();return result;}
static mask(source){const result=this.sample(source),values=this.Input,n=values.length,m=result.length,ways=Array.from({length:n+1},()=>Array(m+1).fill(0));for(let i=0;i<=n;++i)ways[i][m]=1;for(let i=n-1;i>=0;--i)for(let j=m-1;j>=0;--j)ways[i][j]=ways[i+1][j]+(values[i]===result[j]?ways[i+1][j+1]:0);let mask=0,j=0;for(let i=0;i<n;++i){const choose=j<m&&values[i]===result[j]?ways[i+1][j+1]:0,total=ways[i][j];let ticket=0;if(total>1){const bits=Math.ceil(Math.log2(total));do{ticket=0;for(let bit=0;bit<bits;++bit)ticket=(ticket<<1)|source.Next();}while(ticket>=total);}if(ticket<choose){mask|=1<<i;++j;}}return mask;}
static large(){const n=this.Input.length,samples=n>64?128:4096,multiplicities=new Map(),totals=new Map();for(const value of this.Input){multiplicities.set(value,(multiplicities.get(value)||0)+1);totals.set(value,0);}let seed=0x85ebca6b,lengthSum=0,squares=0;const source={Next(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed>>>31;}};for(let trial=0;trial<samples;++trial){const result=this.sample(source);lengthSum+=result.length;squares+=(result.length-n/2)**2;for(const value of result)totals.set(value,totals.get(value)+1);}let statistic=0;for(const [value,m] of multiplicities)statistic+=(totals.get(value)-samples*m/2)**2/(samples*m/4);this.check(statistic<4*totals.size+80,'Subset inclusion frequencies are biased');this.check((lengthSum-samples*n/2)**2/(samples*n/4)<40,'Subset sizes are biased');this.check(squares/(samples*n/4)>0.25&&squares/(samples*n/4)<4,'Subset size variation must reflect independent choices');return {actual:this.LastOutput,mutationOk:true,uniformOk:true};}
}
function ChooseMask13(source){return SubsetState13.mask(source);}
'''
def finish(value):
    value=value.replace('function executeSubset13(row){','function executeSubset13(row){SubsetState13.Input=row.arguments[0].slice();if(SubsetState13.Input.length>5)return SubsetState13.large();')
    value=value.replace('randomCheck([row.arguments[0].map(value=>value+1)])','randomCheck([[]])')
    return value.replace('actual:context.first','actual:SubsetState13.LastOutput')
