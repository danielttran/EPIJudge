"""Concrete vector observations and bounded small-mask probability lifting."""
CORE=r'''
#include <unordered_map>
#include <unordered_set>
namespace SubsetState13 {
static std::vector<int> Input,LastOutput;
void check(bool ok,const std::string& message){if(!ok)throw std::runtime_error(message);}
struct Coins:FairCoinSource {ChoiceBitSource& source;int calls=0;explicit Coins(ChoiceBitSource& source):source(source){}bool Next()override{check(++calls<=64*static_cast<int>(Input.size())+128,"Subset exceeded the supplied-coin budget");return source.Next()==1;}};
std::vector<int> sample(ChoiceBitSource& source){auto values=Input;Coins coins(source);std::vector<int> result=Solution_13_8().RandomSubset(values,coins);check(values==Input,"Preserve input values and order");size_t cursor=0;for(int value:result){while(cursor<values.size()&&values[cursor]!=value)cursor++;check(cursor<values.size(),"Return an ordered subsequence of original occurrences");cursor++;}LastOutput=result;return result;}
int mask(ChoiceBitSource& source){auto result=sample(source);int n=static_cast<int>(Input.size()),m=static_cast<int>(result.size());std::vector<std::vector<int>> ways(n+1,std::vector<int>(m+1));for(int i=0;i<=n;++i)ways[i][m]=1;for(int i=n-1;i>=0;--i)for(int j=m-1;j>=0;--j)ways[i][j]=ways[i+1][j]+(Input[i]==result[j]?ways[i+1][j+1]:0);int mask=0,index=0;for(int i=0;i<n;++i){int choose=index<m&&Input[i]==result[index]?ways[i+1][index+1]:0,total=ways[i][index],ticket=0;if(total>1){int bits=0;for(int maximum=total-1;maximum>0;maximum>>=1)bits++;do{ticket=0;for(int b=0;b<bits;++b)ticket=(ticket<<1)|source.Next();}while(ticket>=total);}if(ticket<choose){mask|=1<<i;index++;}}return mask;}
struct SeedBits:ChoiceBitSource {unsigned int seed=0x85ebca6b;int Next()override{seed=seed*1664525u+1013904223u;return static_cast<int>(seed>>31);}};
json large(){int n=static_cast<int>(Input.size()),samples=n>64?128:4096;std::unordered_map<int,int> multiplicities,totals;for(int value:Input){++multiplicities[value];totals[value]=0;}SeedBits source;double lengthSum=0,squares=0;for(int trial=0;trial<samples;++trial){auto result=sample(source);lengthSum+=result.size();double centered=static_cast<double>(result.size())-n/2.0;squares+=centered*centered;for(int value:result)++totals[value];}double statistic=0;for(const auto& pair:multiplicities){double difference=totals[pair.first]-samples*pair.second/2.0;statistic+=difference*difference/(samples*pair.second/4.0);}check(statistic<4*totals.size()+80,"Subset inclusion frequencies are biased");check((lengthSum-samples*n/2.0)*(lengthSum-samples*n/2.0)/(samples*n/4.0)<40,"Subset sizes are biased");check(squares/(samples*n/4.0)>0.25&&squares/(samples*n/4.0)<4,"Subset size variation must reflect independent choices");return json{{"actual",LastOutput},{"mutationOk",true},{"uniformOk",true}};}
}
struct SubsetSubject13 {int ChooseMask13(ChoiceBitSource& source){return SubsetState13::mask(source);}};
'''
def finish(value):
    value=value.replace('json run(const json& row){','json run(const json& row){SubsetState13::Input=row["arguments"][0].get<std::vector<int>>();if(SubsetState13::Input.size()>5)return SubsetState13::large();')
    value=value.replace('auto values=row["arguments"][0].get<std::vector<int>>();for(auto& value:values)++value;','std::vector<int> values;')
    return value.replace('"actual",First','"actual",SubsetState13::LastOutput')
