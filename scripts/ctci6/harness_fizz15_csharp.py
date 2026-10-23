"""Four actual managed workers, atomic print validation and per-case counting gates."""
CORE=r'''
sealed class FizzState15{
 public readonly object Mutex=new();public readonly int Limit;public readonly System.Threading.SemaphoreSlim[] Gates={new(1),new(0),new(0),new(0)};
 public readonly List<string> Events=new(),Errors=new();public int Next=1;public bool Printing;
 public readonly System.Threading.CountdownEvent Ready=new(4);public readonly System.Threading.ManualResetEventSlim Start=new(false);
 public FizzState15(int limit){Limit=limit;}public static int Owner(int value)=>value%15==0?3:value%3==0?1:value%5==0?2:0;
}
sealed class OwnedFizzContext15:FizzContext{
 readonly FizzState15 state;readonly int role,owner;int calls;
 public OwnedFizzContext15(FizzState15 state,int role){this.state=state;this.role=role;owner=Environment.CurrentManagedThreadId;}
 void Check(int gate=-1){if(owner!=Environment.CurrentManagedThreadId||++calls>4*(state.Limit+1)||gate< -1||gate>3)throw new InvalidOperationException("Invalid synchronization API call");}
 public override void Wait(int gate){Check(gate);if(gate<0||!state.Gates[gate].Wait(1000))throw new InvalidOperationException("Synchronization did not complete");}
 public override void Signal(int gate){Check(gate);if(gate<0)throw new InvalidOperationException("Invalid gate");state.Gates[gate].Release();}
 public override void Print(int value){Check();lock(state.Mutex){if(value<1||value>state.Limit||value!=state.Next||state.Printing||FizzState15.Owner(value)!=role)throw new InvalidOperationException("Wrong printing role, duplicate, overlap or out-of-order item");state.Printing=true;}System.Threading.Thread.Sleep(2);lock(state.Mutex){string text=(value%3==0?"Fizz":"")+(value%5==0?"Buzz":"");state.Events.Add(text.Length>0?text:value.ToString(System.Globalization.CultureInfo.InvariantCulture));state.Next++;state.Printing=false;}}
}
'''
INSIDE=r'''
static object Execute(JsonElement row){var args=row.GetProperty("arguments");int limit=args[0].GetInt32(),mask=args[2].GetInt32();var order=JsonSerializer.Deserialize<int[]>(args[1].GetRawText())!;var state=new FizzState15(limit);
 var threads=order.Select(role=>new System.Threading.Thread(()=>{try{var context=new OwnedFizzContext15(state,role);state.Ready.Signal();if(!state.Start.Wait(1000))throw new Exception("Workers did not start");if(((mask>>role)&1)!=0)System.Threading.Thread.Sleep(4);System.Action<int,int,FizzContext> invoke=new Solution_15_7().RunFizzBuzz;invoke(role,limit,context);}catch(Exception error){lock(state.Mutex)state.Errors.Add(error.Message);}}){IsBackground=true}).ToArray();
 foreach(var thread in threads)thread.Start();bool ready=state.Ready.Wait(1000);state.Start.Set();bool finished=true;foreach(var thread in threads)finished&=thread.Join(1500);lock(state.Mutex)return new {actual=state.Events.ToArray(),mutationOk=ready&&finished&&state.Errors.Count==0&&state.Next==limit+1&&!state.Printing};
}
'''
