"""Full deterministic reveal/flag game transitions, without a console/UI dependency."""
def body(language):
    if language=='python':return '''rows,columns=len(bombs),len(bombs[0])
visible=[[9]*columns for _ in bombs]
safe=sum(value==0 for row in bombs for value in row)
state=0
trace=[]
def snapshot(accepted):
    trace.append([state,accepted]+[v for row in visible for v in row])
def expose(row,column,queue):
    nonlocal safe
    if visible[row][column]!=9 or bombs[row][column]:return
    visible[row][column]=sum(bombs[r][c] for r in range(max(0,row-1),min(rows,row+2)) for c in range(max(0,column-1),min(columns,column+2)))
    safe-=1
    if visible[row][column]==0:queue.append((row,column))
snapshot(0)
for row,column,kind in actions:
    accepted=0
    if state==0 and 0<=row<rows and 0<=column<columns:
        if kind==1 and visible[row][column] in (9,10):
            visible[row][column]=19-visible[row][column]
            accepted=1
        elif kind==0 and visible[row][column]==9:
            accepted=1
            if bombs[row][column]:visible[row][column]=11;state=2
            else:
                queue=[]
                expose(row,column,queue)
                head=0
                while head<len(queue):
                    r,c=queue[head];head+=1
                    for nr in range(max(0,r-1),min(rows,r+2)):
                        for nc in range(max(0,c-1),min(columns,c+2)):expose(nr,nc,queue)
                if safe==0:state=1
    snapshot(accepted)
return trace'''
    if language=='javascript':return '''const rows=bombs.length,columns=bombs[0].length,visible=bombs.map(row=>row.map(()=>9)),trace=[];
let safe=bombs.flat().filter(v=>v===0).length,state=0;
function snapshot(accepted){trace.push([state,accepted,...visible.flat()]);}
function expose(row,column,queue){
 if(visible[row][column]!==9||bombs[row][column])return;
 let number=0;for(let r=Math.max(0,row-1);r<Math.min(rows,row+2);++r)for(let c=Math.max(0,column-1);c<Math.min(columns,column+2);++c)number+=bombs[r][c];
 visible[row][column]=number;--safe;if(number===0)queue.push([row,column]);
}
snapshot(0);
for(const [row,column,kind] of actions){let accepted=0;
 if(state===0&&row>=0&&row<rows&&column>=0&&column<columns){
  if(kind===1&&(visible[row][column]===9||visible[row][column]===10)){visible[row][column]=19-visible[row][column];accepted=1;}
  else if(kind===0&&visible[row][column]===9){accepted=1;
   if(bombs[row][column]){visible[row][column]=11;state=2;}
   else{const queue=[];expose(row,column,queue);for(let head=0;head<queue.length;++head){const [r,c]=queue[head];for(let nr=Math.max(0,r-1);nr<Math.min(rows,r+2);++nr)for(let nc=Math.max(0,c-1);nc<Math.min(columns,c+2);++nc)expose(nr,nc,queue);}if(safe===0)state=1;}
  }
 }
 snapshot(accepted);
}
return trace;'''
    if language=='cpp':return '''int rows=bombs.size(),columns=bombs[0].size(),safe=0,state=0;
for(const auto& row:bombs)for(int v:row)if(v==0)++safe;
std::vector<std::vector<int>> visible(rows,std::vector<int>(columns,9)),trace;
auto snapshot=[&](int accepted){std::vector<int> result{state,accepted};for(const auto& row:visible)result.insert(result.end(),row.begin(),row.end());trace.push_back(std::move(result));};
auto expose=[&](int row,int column,std::vector<std::pair<int,int>>& queue){
 if(visible[row][column]!=9||bombs[row][column])return;
 int number=0;for(int r=std::max(0,row-1);r<std::min(rows,row+2);++r)for(int c=std::max(0,column-1);c<std::min(columns,column+2);++c)number+=bombs[r][c];
 visible[row][column]=number;--safe;if(number==0)queue.push_back({row,column});
};
snapshot(0);
for(const auto& action:actions){int row=action[0],column=action[1],kind=action[2],accepted=0;
 if(state==0&&row>=0&&row<rows&&column>=0&&column<columns){
  if(kind==1&&(visible[row][column]==9||visible[row][column]==10)){visible[row][column]=19-visible[row][column];accepted=1;}
  else if(kind==0&&visible[row][column]==9){accepted=1;
   if(bombs[row][column]){visible[row][column]=11;state=2;}
   else{std::vector<std::pair<int,int>> queue;expose(row,column,queue);for(size_t head=0;head<queue.size();++head){auto [r,c]=queue[head];for(int nr=std::max(0,r-1);nr<std::min(rows,r+2);++nr)for(int nc=std::max(0,c-1);nc<std::min(columns,c+2);++nc)expose(nr,nc,queue);}if(safe==0)state=1;}
  }
 }
 snapshot(accepted);
}
return trace;'''
    java=language=='java'
    return ('''int rows=bombs.length,columns=bombs[0].length;
int[][] visible=new int[rows][columns];for(int[] row:visible)Arrays.fill(row,9);
int[] remaining={0},state={0};for(int[] row:bombs)for(int value:row)if(value==0)remaining[0]++;
var trace=new ArrayList<int[]>();
class Observer{
 void snapshot(int accepted){int[] result=new int[2+rows*columns];result[0]=state[0];result[1]=accepted;for(int r=0;r<rows;r++)for(int c=0;c<columns;c++)result[2+r*columns+c]=visible[r][c];trace.add(result);}
 void expose(int row,int column,ArrayList<int[]> queue){
''' if java else '''int rows=bombs.Length,columns=bombs[0].Length;
var visible=Enumerable.Range(0,rows).Select(_=>Enumerable.Repeat(9,columns).ToArray()).ToArray();
int remaining=0,state=0;foreach(var row in bombs)foreach(int value in row)if(value==0)remaining++;
var trace=new List<int[]>();
void Snapshot(int accepted){var result=new int[2+rows*columns];result[0]=state;result[1]=accepted;for(int r=0;r<rows;r++)for(int c=0;c<columns;c++)result[2+r*columns+c]=visible[r][c];trace.Add(result);}
void Expose(int row,int column,List<int[]> queue){
''')+''' if(visible[row][column]!=9||bombs[row][column]!=0)return;
 int number=0;for(int r=Math.max(0,row-1);r<Math.min(rows,row+2);++r)for(int c=Math.max(0,column-1);c<Math.min(columns,column+2);++c)number+=bombs[r][c];
 visible[row][column]=number;--REMAINING;if(number==0)queue.ADD(new int[]{row,column});
}
'''.replace('Math.max','Math.max' if java else 'Math.Max').replace('Math.min','Math.min' if java else 'Math.Min').replace('REMAINING','remaining[0]' if java else 'remaining').replace('ADD','add' if java else 'Add')+('}\nvar observer=new Observer();\n' if java else '')+'''SNAPSHOT(0);
LOOP{
 int row=action[0],column=action[1],kind=action[2],accepted=0;
 if(STATE==0&&row>=0&&row<rows&&column>=0&&column<columns){
  if(kind==1&&(visible[row][column]==9||visible[row][column]==10)){visible[row][column]=19-visible[row][column];accepted=1;}
  else if(kind==0&&visible[row][column]==9){accepted=1;
   if(bombs[row][column]!=0){visible[row][column]=11;STATE=2;}
   else{var queue=new QUEUE();EXPOSE(row,column,queue);for(int head=0;head<COUNT;++head){int r=queue.GET[0],c=queue.GET[1];for(int nr=Math.max(0,r-1);nr<Math.min(rows,r+2);++nr)for(int nc=Math.max(0,c-1);nc<Math.min(columns,c+2);++nc)EXPOSE(nr,nc,queue);}if(REMAINING==0)STATE=1;}
  }
 }
 SNAPSHOT(accepted);
}
RETURN;
'''.replace('LOOP','for(int[] action:actions)' if java else 'foreach(var action in actions)').replace('STATE','state[0]' if java else 'state').replace('REMAINING','remaining[0]' if java else 'remaining').replace('SNAPSHOT','observer.snapshot' if java else 'Snapshot').replace('EXPOSE','observer.expose' if java else 'Expose').replace('QUEUE','ArrayList<int[]>' if java else 'List<int[]>').replace('COUNT','queue.size()' if java else 'queue.Count').replace('GET','get(head)' if java else '[head]').replace('Math.max','Math.max' if java else 'Math.Max').replace('Math.min','Math.min' if java else 'Math.Min').replace('RETURN','return trace.toArray(new int[0][])' if java else 'return trace.ToArray()').replace('queue.[head]','queue[head]')
