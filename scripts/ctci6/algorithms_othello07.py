"""Independent legal-ray capture and automatic-pass Othello engine."""
def body(language):
 if language=='python':return '''board=[[0]*size for _ in range(size)]
middle=size//2
board[middle-1][middle-1]=board[middle][middle]=2
board[middle-1][middle]=board[middle][middle-1]=1
trace=[]
def captures(row,column,color):
    if not (0<=row<size and 0<=column<size) or board[row][column]!=0:return []
    result=[]
    for dr in (-1,0,1):
        for dc in (-1,0,1):
            if dr==dc==0:continue
            r,c=row+dr,column+dc
            path=[]
            while 0<=r<size and 0<=c<size and board[r][c]==3-color:
                path.append((r,c));r+=dr;c+=dc
            if path and 0<=r<size and 0<=c<size and board[r][c]==color:result.extend(path)
    return result
def can_move(color):
    return any(captures(r,c,color) for r in range(size) for c in range(size))
def snapshot(accepted):
    flat=[v for row in board for v in row]
    trace.append([turn,accepted,flat.count(1),flat.count(2)]+flat)
turn=1 if can_move(1) else 0
snapshot(0)
for row,column,color in actions:
    accepted=0
    if turn and color==turn:
        flipped=captures(row,column,color)
        if flipped:
            board[row][column]=color
            for r,c in flipped:board[r][c]=color
            accepted=1
            turn=3-color if can_move(3-color) else color if can_move(color) else 0
    snapshot(accepted)
return trace'''
 if language=='javascript':return '''const board=Array.from({length:size},()=>Array(size).fill(0)),middle=Math.floor(size/2),trace=[];
board[middle-1][middle-1]=board[middle][middle]=2;board[middle-1][middle]=board[middle][middle-1]=1;
function captures(row,column,color){
 if(row<0||row>=size||column<0||column>=size||board[row][column]!==0)return [];
 const result=[];
 for(let dr=-1;dr<=1;++dr)for(let dc=-1;dc<=1;++dc){if(dr===0&&dc===0)continue;let r=row+dr,c=column+dc;const path=[];
  while(r>=0&&r<size&&c>=0&&c<size&&board[r][c]===3-color){path.push([r,c]);r+=dr;c+=dc;}
  if(path.length&&r>=0&&r<size&&c>=0&&c<size&&board[r][c]===color)result.push(...path);
 }
 return result;
}
function canMove(color){for(let r=0;r<size;++r)for(let c=0;c<size;++c)if(captures(r,c,color).length)return true;return false;}
let turn=canMove(1)?1:0;
function snapshot(accepted){const flat=board.flat();trace.push([turn,accepted,flat.filter(v=>v===1).length,flat.filter(v=>v===2).length,...flat]);}
snapshot(0);
for(const [row,column,color] of actions){let accepted=0;if(turn&&color===turn){const flipped=captures(row,column,color);if(flipped.length){board[row][column]=color;for(const [r,c] of flipped)board[r][c]=color;accepted=1;turn=canMove(3-color)?3-color:canMove(color)?color:0;}}snapshot(accepted);}
return trace;'''
 if language=='cpp':return '''std::vector<std::vector<int>> board(size,std::vector<int>(size)),trace;
int middle=size/2;board[middle-1][middle-1]=board[middle][middle]=2;board[middle-1][middle]=board[middle][middle-1]=1;
auto captures=[&](int row,int column,int color){
 std::vector<std::pair<int,int>> result;
 if(row<0||row>=size||column<0||column>=size||board[row][column]!=0)return result;
 for(int dr=-1;dr<=1;++dr)for(int dc=-1;dc<=1;++dc){if(dr==0&&dc==0)continue;int r=row+dr,c=column+dc;std::vector<std::pair<int,int>> path;
  while(r>=0&&r<size&&c>=0&&c<size&&board[r][c]==3-color){path.push_back({r,c});r+=dr;c+=dc;}
  if(!path.empty()&&r>=0&&r<size&&c>=0&&c<size&&board[r][c]==color)result.insert(result.end(),path.begin(),path.end());
 }
 return result;
};
auto canMove=[&](int color){for(int r=0;r<size;++r)for(int c=0;c<size;++c)if(!captures(r,c,color).empty())return true;return false;};
int turn=canMove(1)?1:0;
auto snapshot=[&](int accepted){int black=0,white=0;for(const auto& row:board)for(int v:row){black+=v==1;white+=v==2;}std::vector<int> result{turn,accepted,black,white};for(const auto& row:board)result.insert(result.end(),row.begin(),row.end());trace.push_back(std::move(result));};
snapshot(0);
for(const auto& action:actions){int row=action[0],column=action[1],color=action[2],accepted=0;
 if(turn&&color==turn){auto flipped=captures(row,column,color);if(!flipped.empty()){board[row][column]=color;for(auto [r,c]:flipped)board[r][c]=color;accepted=1;turn=canMove(3-color)?3-color:canMove(color)?color:0;}}
 snapshot(accepted);
}
return trace;'''
 java=language=='java'
 return ('''int[][] board=new int[size][size];var trace=new ArrayList<int[]>();int middle=size/2;
board[middle-1][middle-1]=board[middle][middle]=2;board[middle-1][middle]=board[middle][middle-1]=1;
class Rules{
 ArrayList<int[]> captures(int row,int column,int color){
''' if java else '''var board=Enumerable.Range(0,size).Select(_=>new int[size]).ToArray();var trace=new List<int[]>();int middle=size/2;
board[middle-1][middle-1]=board[middle][middle]=2;board[middle-1][middle]=board[middle][middle-1]=1;
List<int[]> Captures(int row,int column,int color){
''')+''' var result=new LIST();
 if(row<0||row>=size||column<0||column>=size||board[row][column]!=0)return result;
 for(int dr=-1;dr<=1;++dr)for(int dc=-1;dc<=1;++dc){if(dr==0&&dc==0)continue;int r=row+dr,c=column+dc;var path=new LIST();
  while(r>=0&&r<size&&c>=0&&c<size&&board[r][c]==3-color){path.ADD(new int[]{r,c});r+=dr;c+=dc;}
  if(path.COUNT>0&&r>=0&&r<size&&c>=0&&c<size&&board[r][c]==color)result.ADDALL(path);
 }
 return result;
}
BOOL CANMOVE(int color){for(int r=0;r<size;++r)for(int c=0;c<size;++c)if(CAPTURES(r,c,color).COUNT>0)return true;return false;}
'''.replace('LIST','ArrayList<int[]>' if java else 'List<int[]>').replace('ADDALL','addAll' if java else 'AddRange').replace('ADD','add' if java else 'Add').replace('COUNT','size()' if java else 'Count').replace('BOOL','boolean' if java else 'bool').replace('CANMOVE','canMove' if java else 'CanMove').replace('CAPTURES','captures' if java else 'Captures')+('}\nvar rules=new Rules();\n' if java else '')+'''int turn=CANMOVE(1)?1:0;
SNAP_DECL{
 int black=0,white=0;ROWLOOP VALUELOOP {if(v==1)black++;if(v==2)white++;}
 var result=new int[4+size*size];result[0]=TURN;result[1]=accepted;result[2]=black;result[3]=white;for(int r=0;r<size;r++)for(int c=0;c<size;c++)result[4+r*size+c]=board[r][c];trace.ADD(result);
}
SNAP_CALL(0);
ACTIONLOOP{
 int row=action[0],column=action[1],color=action[2],accepted=0;
 if(turn!=0&&color==turn){var flipped=CAPTURES(row,column,color);if(flipped.COUNT>0){board[row][column]=color;FLIPLOOP board[p[0]][p[1]]=color;accepted=1;turn=CANMOVE(3-color)?3-color:CANMOVE(color)?color:0;}}
 SNAP_CALL(accepted);
}
RESULT;
'''.replace('SNAP_DECL','class Snapshotter{void snapshot(int accepted,int currentTurn)' if java else 'void Snapshot(int accepted)').replace('TURN','currentTurn' if java else 'turn').replace('ROWLOOP','for(int[] row:board)' if java else 'foreach(var row in board)').replace('VALUELOOP','for(int v:row)' if java else 'foreach(int v in row)').replace('ADD','add' if java else 'Add').replace('}\nSNAP_CALL(0);','}}\nvar observer=new Snapshotter();\nSNAP_CALL(0);' if java else '}\nSNAP_CALL(0);').replace('SNAP_CALL(accepted)','observer.snapshot(accepted,turn)' if java else 'Snapshot(accepted)').replace('SNAP_CALL(0)','observer.snapshot(0,turn)' if java else 'Snapshot(0)').replace('ACTIONLOOP','for(int[] action:actions)' if java else 'foreach(var action in actions)').replace('FLIPLOOP','for(int[] p:flipped)' if java else 'foreach(var p in flipped)').replace('CAPTURES','rules.captures' if java else 'Captures').replace('CANMOVE','rules.canMove' if java else 'CanMove').replace('COUNT','size()' if java else 'Count').replace('RESULT','return trace.toArray(new int[0][])' if java else 'return trace.ToArray()')
