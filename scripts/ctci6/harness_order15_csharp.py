"""Real managed threads; completion checks do not order user work automatically."""
CORE=r'''
sealed class OrderState15 {
 public readonly object Mutex=new();public readonly System.Threading.SemaphoreSlim[] Gates={new(0),new(0)};
 public readonly bool[] Complete=new bool[3],Invoked=new bool[3];public readonly List<int> Events=new();public readonly List<string> Errors=new();
 public readonly System.Threading.CountdownEvent Ready=new(3);public readonly System.Threading.ManualResetEventSlim Start=new(false);
}
sealed class OwnedOrderContext15:SyncContext {
 readonly OrderState15 state;readonly int role,owner;int calls;
 public OwnedOrderContext15(OrderState15 state,int role){this.state=state;this.role=role;owner=Environment.CurrentManagedThreadId;}
 void Check(int gate=-1){if(owner!=Environment.CurrentManagedThreadId||++calls>20||gate< -1||gate>1)throw new InvalidOperationException("Invalid synchronization API call");}
 public override void Wait(int gate){Check(gate);if(gate<0||!state.Gates[gate].Wait(1000))throw new InvalidOperationException("Synchronization did not complete");}
 public override void Signal(int gate){Check(gate);if(gate<0)throw new InvalidOperationException("Invalid gate");state.Gates[gate].Release();}
 public override void Work(){Check();lock(state.Mutex){if(state.Invoked[role]||role>0&&!state.Complete[role-1])throw new InvalidOperationException("Work started before predecessor completion or ran twice");state.Invoked[role]=true;state.Events.Add(role);}System.Threading.Thread.Sleep(2);lock(state.Mutex)state.Complete[role]=true;}
}
'''
INSIDE=r'''
static object Execute(JsonElement row){
 var args=row.GetProperty("arguments");var order=JsonSerializer.Deserialize<int[]>(args[0].GetRawText())!;int mask=args[1].GetInt32();var state=new OrderState15();
 var threads=order.Select(role=>new System.Threading.Thread(()=>{try{var context=new OwnedOrderContext15(state,role);state.Ready.Signal();if(!state.Start.Wait(1000))throw new Exception("Workers did not start");if(((mask>>role)&1)!=0)System.Threading.Thread.Sleep(4);System.Action<int,SyncContext> invoke=new Solution_15_5().RunOrdered;invoke(role,context);}catch(Exception error){lock(state.Mutex)state.Errors.Add(error.Message);}}){IsBackground=true}).ToArray();
 foreach(var thread in threads)thread.Start();bool ready=state.Ready.Wait(1000);state.Start.Set();bool finished=true;foreach(var thread in threads)finished&=thread.Join(1500);
 lock(state.Mutex)return new {actual=state.Events.ToArray(),mutationOk=ready&&finished&&state.Errors.Count==0&&state.Complete.All(v=>v)};
}
'''
