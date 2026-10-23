"""Independent exhaustive oriented-piece assembly; no original-coordinate hints."""
def body(language):
    if language=='python':return '''count=len(pieces)
placed=[None]*count
used=[False]*count
def edge(index,turn,side):
    return pieces[index][(side-turn)%4]
def search(position):
    if position==count:return True
    row,column=divmod(position,size)
    for index in range(count):
        if used[index]:continue
        for turn in range(4):
            values=[edge(index,turn,s) for s in range(4)]
            if any((value==0)!=boundary for value,boundary in zip(values,(row==0,column==size-1,row==size-1,column==0))):continue
            if row and values[0]!=-edge(*placed[position-size],2):continue
            if column and values[3]!=-edge(*placed[position-1],1):continue
            used[index]=True
            placed[position]=(index,turn)
            if search(position+1):return True
            used[index]=False
    return False
return [list(pair) for pair in placed] if search(0) else []'''
    if language=='javascript':return '''const count=pieces.length,placed=Array(count),used=Array(count).fill(false);
const edge=(index,turn,side)=>pieces[index][(side-turn+4)%4];
function search(position){
 if(position===count)return true;
 const row=Math.floor(position/size),column=position%size;
 for(let index=0;index<count;++index){if(used[index])continue;
  for(let turn=0;turn<4;++turn){const values=[0,1,2,3].map(s=>edge(index,turn,s)),bounds=[row===0,column===size-1,row===size-1,column===0];
   if(values.some((v,s)=>(v===0)!==bounds[s]))continue;
   if(row&&values[0]!==-edge(...placed[position-size],2))continue;
   if(column&&values[3]!==-edge(...placed[position-1],1))continue;
   used[index]=true;placed[position]=[index,turn];
   if(search(position+1))return true;
   used[index]=false;
  }
 }
 return false;
}
return search(0)?placed:[];'''
    if language=='cpp':return '''int count=static_cast<int>(pieces.size());
std::vector<std::vector<int>> placed(count,std::vector<int>(2));
std::vector<bool> used(count,false);
auto edge=[&](int index,int turn,int side){return pieces[index][(side-turn+4)%4];};
std::function<bool(int)> search=[&](int position){
 if(position==count)return true;
 int row=position/size,column=position%size;
 for(int index=0;index<count;++index){if(used[index])continue;
  for(int turn=0;turn<4;++turn){int values[4];bool bounds[4]={row==0,column==size-1,row==size-1,column==0},fits=true;
   for(int side=0;side<4;++side){values[side]=edge(index,turn,side);if((values[side]==0)!=bounds[side])fits=false;}
   if(!fits)continue;
   if(row&&values[0]!=-edge(placed[position-size][0],placed[position-size][1],2))continue;
   if(column&&values[3]!=-edge(placed[position-1][0],placed[position-1][1],1))continue;
   used[index]=true;placed[position]={index,turn};
   if(search(position+1))return true;
   used[index]=false;
  }
 }
 return false;
};
return search(0)?placed:std::vector<std::vector<int>>{};'''
    java=language=='java'
    return ('''int count=pieces.Length;
var placed=Enumerable.Range(0,count).Select(_=>new int[2]).ToArray();
var used=new bool[count];
int Edge(int index,int turn,int side)=>pieces[index][(side-turn+4)%4];
bool Search(int position){
''' if not java else '''int count=pieces.length;
int[][] placed=new int[count][2];
boolean[] used=new boolean[count];
class Searcher{
 int edge(int index,int turn,int side){return pieces[index][(side-turn+4)%4];}
 boolean search(int position){
''')+''' if(position==count)return true;
 int row=position/size,column=position%size;
 for(int index=0;index<count;++index){if(used[index])continue;
  for(int turn=0;turn<4;++turn){int[] values=new int[4];BOOL[] bounds={row==0,column==size-1,row==size-1,column==0};BOOL fits=true;
   for(int side=0;side<4;++side){values[side]=EDGE(index,turn,side);if((values[side]==0)!=bounds[side])fits=false;}
   if(!fits)continue;
   if(row>0&&values[0]!=-EDGE(placed[position-size][0],placed[position-size][1],2))continue;
   if(column>0&&values[3]!=-EDGE(placed[position-1][0],placed[position-1][1],1))continue;
   used[index]=true;placed[position][0]=index;placed[position][1]=turn;
   if(SEARCH(position+1))return true;
   used[index]=false;
  }
 }
 return false;
}
'''.replace('BOOL','boolean' if java else 'bool').replace('EDGE','edge' if java else 'Edge').replace('SEARCH','search' if java else 'Search')+('}\nreturn new Searcher().search(0)?placed:new int[0][];' if java else 'return Search(0)?placed:Array.Empty<int[]>();')
