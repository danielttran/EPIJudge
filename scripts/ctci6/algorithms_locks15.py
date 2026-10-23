"""Transactional per-owner declaration graph rebuilt before transitive-closure admission."""
def body(language):
 if language=='python':return '''class DeadlockFreeLocks:
    def __init__(self,resourceCount: int,pool: LockPool):
        self._count=resourceCount
        self._pool=pool
        self._orders=[[] for _ in range(4)]
        self._next=[0]*4
    def Declare(self,owner: int,order: list[int]) -> bool:
        if not 0<=owner<4:return False
        seen=[False]*self._count
        for resource in order:
            if not 0<=resource<self._count or seen[resource]:return False
            seen[resource]=True
        reach=[[False]*self._count for _ in range(self._count)]
        for candidate in range(4):
            path=order if candidate==owner else self._orders[candidate]
            for first,second in zip(path,path[1:]):reach[first][second]=True
        for middle in range(self._count):
            for first in range(self._count):
                for second in range(self._count):
                    reach[first][second] |= reach[first][middle] and reach[middle][second]
        if any(reach[i][i] for i in range(self._count)):return False
        self._orders[owner]=order.copy()
        self._next[owner]=0
        return True
    def GetLock(self,owner: int,resource: int) -> ResourceLock | None:
        if not 0<=owner<4:return None
        path=self._orders[owner]
        position=self._next[owner]
        if position==len(path) or path[position]!=resource:return None
        self._next[owner]+=1
        return self._pool.Get(resource)
'''
 if language=='javascript':return '''class DeadlockFreeLocks {
 constructor(resourceCount,pool){this.count=resourceCount;this.pool=pool;this.orders=Array.from({length:4},()=>[]);this.next=Array(4).fill(0);}
 Declare(owner,order){
  if(owner<0||owner>=4)return false;const seen=Array(this.count).fill(false);
  for(const resource of order){if(resource<0||resource>=this.count||seen[resource])return false;seen[resource]=true;}
  const reach=Array.from({length:this.count},()=>Array(this.count).fill(false));
  for(let candidate=0;candidate<4;++candidate){const path=candidate===owner?order:this.orders[candidate];for(let i=1;i<path.length;++i)reach[path[i-1]][path[i]]=true;}
  for(let middle=0;middle<this.count;++middle)for(let first=0;first<this.count;++first)for(let second=0;second<this.count;++second)reach[first][second]=reach[first][second]||(reach[first][middle]&&reach[middle][second]);
  for(let i=0;i<this.count;++i)if(reach[i][i])return false;
  this.orders[owner]=order.slice();this.next[owner]=0;return true;
 }
 GetLock(owner,resource){if(owner<0||owner>=4)return null;const path=this.orders[owner],position=this.next[owner];if(position===path.length||path[position]!==resource)return null;++this.next[owner];return this.pool.Get(resource);}
}'''
 if language=='cpp':return '''class DeadlockFreeLocks {
 int count;LockPool& pool;std::array<std::vector<int>,4> orders;std::array<std::size_t,4> next{};
public:
 DeadlockFreeLocks(int resourceCount,LockPool& pool):count(resourceCount),pool(pool){}
 bool Declare(int owner,const std::vector<int>& order){
  if(owner<0||owner>=4)return false;std::vector<bool> seen(count,false);
  for(int resource:order){if(resource<0||resource>=count||seen[resource])return false;seen[resource]=true;}
  std::vector<std::vector<bool>> reach(count,std::vector<bool>(count,false));
  for(int candidate=0;candidate<4;++candidate){const auto& path=candidate==owner?order:orders[candidate];for(std::size_t i=1;i<path.size();++i)reach[path[i-1]][path[i]]=true;}
  for(int middle=0;middle<count;++middle)for(int first=0;first<count;++first)for(int second=0;second<count;++second)reach[first][second]=reach[first][second]||(reach[first][middle]&&reach[middle][second]);
  for(int i=0;i<count;++i)if(reach[i][i])return false;
  orders[owner]=order;next[owner]=0;return true;
 }
 ResourceLock* GetLock(int owner,int resource){if(owner<0||owner>=4)return nullptr;const auto& path=orders[owner];if(next[owner]==path.size()||path[next[owner]]!=resource)return nullptr;++next[owner];return pool.Get(resource);}
};'''
 if language=='csharp':return '''public class DeadlockFreeLocks {
 private readonly int count;private readonly LockPool pool;private readonly int[][] orders=Enumerable.Range(0,4).Select(_=>Array.Empty<int>()).ToArray();private readonly int[] next=new int[4];
 public DeadlockFreeLocks(int resourceCount,LockPool pool){count=resourceCount;this.pool=pool;}
 public bool Declare(int owner,int[] order){
  if(owner<0||owner>=4)return false;var seen=new bool[count];foreach(int resource in order){if(resource<0||resource>=count||seen[resource])return false;seen[resource]=true;}
  var reach=new bool[count,count];for(int candidate=0;candidate<4;++candidate){var path=candidate==owner?order:orders[candidate];for(int i=1;i<path.Length;++i)reach[path[i-1],path[i]]=true;}
  for(int middle=0;middle<count;++middle)for(int first=0;first<count;++first)for(int second=0;second<count;++second)reach[first,second]|=reach[first,middle]&&reach[middle,second];
  for(int i=0;i<count;++i)if(reach[i,i])return false;orders[owner]=order.ToArray();next[owner]=0;return true;
 }
 public ResourceLock? GetLock(int owner,int resource){if(owner<0||owner>=4)return null;var path=orders[owner];if(next[owner]==path.Length||path[next[owner]]!=resource)return null;next[owner]++;return pool.Get(resource);}
}'''
 return '''class DeadlockFreeLocks {
 private final int count;private final LockPool pool;private final int[][] orders=new int[4][0];private final int[] next=new int[4];
 public DeadlockFreeLocks(int resourceCount,LockPool pool){count=resourceCount;this.pool=pool;}
 public boolean Declare(int owner,int[] order){
  if(owner<0||owner>=4)return false;boolean[] seen=new boolean[count];for(int resource:order){if(resource<0||resource>=count||seen[resource])return false;seen[resource]=true;}
  boolean[][] reach=new boolean[count][count];for(int candidate=0;candidate<4;++candidate){int[] path=candidate==owner?order:orders[candidate];for(int i=1;i<path.length;++i)reach[path[i-1]][path[i]]=true;}
  for(int middle=0;middle<count;++middle)for(int first=0;first<count;++first)for(int second=0;second<count;++second)reach[first][second]|=reach[first][middle]&&reach[middle][second];
  for(int i=0;i<count;++i)if(reach[i][i])return false;orders[owner]=order.clone();next[owner]=0;return true;
 }
 public ResourceLock GetLock(int owner,int resource){if(owner<0||owner>=4)return null;int[] path=orders[owner];if(next[owner]==path.length||path[next[owner]]!=resource)return null;next[owner]++;return pool.Get(resource);}
}'''
