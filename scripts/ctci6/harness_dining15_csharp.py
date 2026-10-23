"""Actual managed threads and exclusive fork semaphores, without forced eating order."""
CORE=r'''
sealed class DiningState15{
 public readonly object Mutex=new();public readonly int N,Bites;public readonly System.Threading.SemaphoreSlim[] Gates;public readonly int[] Owners,Meals,FirstForks;public readonly bool[] FirstAcquired;public readonly System.Threading.ManualResetEventSlim Phase=new(false);public readonly List<int> Events=new();public readonly List<string> Errors=new();
 public readonly System.Threading.CountdownEvent Ready;public readonly System.Threading.ManualResetEventSlim Start=new(false);
 public DiningState15(int n,int bites){N=n;Bites=bites;Gates=Enumerable.Range(0,n).Select(_=>new System.Threading.SemaphoreSlim(1)).ToArray();Owners=Enumerable.Repeat(-1,n).ToArray();Meals=new int[n];FirstForks=Enumerable.Repeat(-1,n).ToArray();FirstAcquired=new bool[n];Ready=new(n);}
 public void CheckPhase(){if(Enumerable.Range(0,N).All(r=>FirstForks[r]>=0&&(FirstAcquired[r]||Owners[FirstForks[r]]!= -1)))Phase.Set();}
}
sealed class OwnedForkContext15:ForkContext{
 readonly DiningState15 state;readonly int role,owner;int calls;
 public OwnedForkContext15(DiningState15 state,int role){this.state=state;this.role=role;owner=Environment.CurrentManagedThreadId;}
 void Check(int fork=-1){if(owner!=Environment.CurrentManagedThreadId||++calls>10000*(state.Bites+1)||fork!= -1&&fork!=role&&fork!=(role+1)%state.N)throw new InvalidOperationException("Use only owned worker and adjacent fork API");}
 public override void Take(int fork){Check(fork);bool first;lock(state.Mutex){first=state.FirstForks[role]<0;if(first)state.FirstForks[role]=fork;state.CheckPhase();}if(fork<0||!state.Gates[fork].Wait(1000))throw new InvalidOperationException("Fork acquisition did not complete");lock(state.Mutex){if(state.Owners[fork]!= -1)throw new InvalidOperationException("Fork lock was not exclusive");state.Owners[fork]=role;if(first)state.FirstAcquired[role]=true;state.CheckPhase();}if(first&&!state.Phase.Wait(1000))throw new InvalidOperationException("Initial acquisition schedule did not complete");}
 public override void Drop(int fork){Check(fork);lock(state.Mutex){if(fork<0||state.Owners[fork]!=role)throw new InvalidOperationException("Release only a held fork");state.Owners[fork]= -1;}state.Gates[fork].Release();}
 public override void Eat(){Check();lock(state.Mutex){if(state.Owners[role]!=role||state.Owners[(role+1)%state.N]!=role||state.Meals[role]>=state.Bites)throw new InvalidOperationException("Eat exactly the requested bites while holding both adjacent forks");state.Meals[role]++;state.Events.Add(role);}System.Threading.Thread.Sleep(2);}
}
'''
INSIDE=r'''
static object Execute(JsonElement row){var args=row.GetProperty("arguments");int n=args[0].GetInt32(),bites=args[1].GetInt32(),mask=args[3].GetInt32();var order=JsonSerializer.Deserialize<int[]>(args[2].GetRawText())!;var state=new DiningState15(n,bites);
 var threads=order.Select(role=>new System.Threading.Thread(()=>{try{var context=new OwnedForkContext15(state,role);state.Ready.Signal();if(!state.Start.Wait(1000))throw new Exception("Workers did not start");if(((mask>>role)&1)!=0)System.Threading.Thread.Sleep(4);System.Action<int,int,int,ForkContext> invoke=new Solution_15_3().Dine;invoke(role,n,bites,context);}catch(Exception error){lock(state.Mutex)state.Errors.Add(error.Message);}}){IsBackground=true}).ToArray();
 foreach(var thread in threads)thread.Start();bool ready=state.Ready.Wait(1000);state.Start.Set();bool finished=true;foreach(var thread in threads)finished&=thread.Join(1500);lock(state.Mutex)return new {actual=state.Events.ToArray(),mutationOk=ready&&finished&&state.Errors.Count==0&&state.Meals.All(v=>v==bites)&&state.Owners.All(v=>v== -1)};
}
'''
