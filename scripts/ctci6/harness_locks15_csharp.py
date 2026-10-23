"""Stable provided lock objects and real concurrent clients of granted lock orders."""
CORE=r'''
sealed class ResourceState15{
 public static readonly System.Threading.ThreadLocal<int> Current=new(()=> -1);
 public readonly object Mutex=new();public readonly System.Threading.SemaphoreSlim[] Gates;public readonly int[] Owners,FirstForks=Enumerable.Repeat(-1,4).ToArray();public readonly bool[] Eligible=new bool[4],FirstAcquired=new bool[4];
 public readonly List<string> Errors=new();public readonly System.Threading.ManualResetEventSlim Phase=new(false),Start=new(false);public readonly System.Threading.CountdownEvent Ready=new(4);
 public ResourceState15(int count){Gates=Enumerable.Range(0,count).Select(_=>new System.Threading.SemaphoreSlim(1)).ToArray();Owners=Enumerable.Repeat(-1,count).ToArray();}
 public void CheckPhase(){if(Enumerable.Range(0,4).All(r=>!Eligible[r]||FirstForks[r]>=0&&(FirstAcquired[r]||Owners[FirstForks[r]]!= -1)))Phase.Set();}
}
sealed class NativeResourceLock15:ResourceLock{
 readonly ResourceState15 state;readonly int resource;
 public NativeResourceLock15(ResourceState15 state,int resource){this.state=state;this.resource=resource;}
 public override void Lock(){int role=ResourceState15.Current.Value;if(role<0||role>=4)throw new InvalidOperationException("Acquire only in registered native clients");bool first;lock(state.Mutex){first=state.FirstForks[role]<0;if(first)state.FirstForks[role]=resource;state.CheckPhase();}if(!state.Gates[resource].Wait(1000))throw new InvalidOperationException("Granted lock orders deadlocked");lock(state.Mutex){if(state.Owners[resource]!= -1)throw new InvalidOperationException("Native lock was not exclusive");state.Owners[resource]=role;if(first)state.FirstAcquired[role]=true;state.CheckPhase();}if(first&&!state.Phase.Wait(1000))throw new InvalidOperationException("Initial acquisition schedule did not complete");}
 public override void Unlock(){int role=ResourceState15.Current.Value;lock(state.Mutex){if(role<0||state.Owners[resource]!=role)throw new InvalidOperationException("Release only held native locks");state.Owners[resource]= -1;}state.Gates[resource].Release();}
}
sealed class NativeLockPool15:LockPool{
 readonly NativeResourceLock15[] locks;
 public NativeLockPool15(ResourceState15 state,int count){locks=Enumerable.Range(0,count).Select(r=>new NativeResourceLock15(state,r)).ToArray();}
 public override ResourceLock Get(int resource){if(resource<0||resource>=locks.Length)throw new ArgumentOutOfRangeException(nameof(resource));return locks[resource];}
}
'''
INSIDE=r'''
static object Execute(JsonElement row){var args=row.GetProperty("arguments");int count=args[0].GetInt32();var state=new ResourceState15(count);var pool=new NativeLockPool15(state,count);var factory=new DeadlockFreeLocks(count,pool);var admitted=new List<bool>();var grants=new List<bool>();var plans=Enumerable.Range(0,4).Select(_=>new List<ResourceLock>()).ToArray();bool valid=true;
 foreach(var declaration in args[1].EnumerateArray()){var values=JsonSerializer.Deserialize<int[]>(declaration.GetRawText())!;int owner=values[0];var order=values.Skip(1).ToArray();var before=order.ToArray();bool decision=factory.Declare(owner,order);admitted.Add(decision);valid&=order.SequenceEqual(before);Array.Fill(order,-999);}
 var other=new DeadlockFreeLocks(count,pool);for(int owner=0;owner<4;owner++)for(int resource=0;resource<count;resource++)valid&=other.GetLock(owner,resource) is null;
 foreach(var request in args[2].EnumerateArray()){int owner=request[0].GetInt32(),resource=request[1].GetInt32();ResourceLock? granted=factory.GetLock(owner,resource);grants.Add(granted is not null);if(granted is not null){if(owner<0||owner>=4||resource<0||resource>=count||!ReferenceEquals(granted,pool.Get(resource)))valid=false;else plans[owner].Add(granted);}}
 if(valid&&plans.Any(plan=>plan.Count>0)){
  for(int owner=0;owner<4;owner++)state.Eligible[owner]=plans[owner].Count>0;
  var threads=Enumerable.Range(0,4).Select(owner=>new System.Threading.Thread(()=>{var acquired=new List<ResourceLock>();try{ResourceState15.Current.Value=owner;state.Ready.Signal();if(!state.Start.Wait(1000))throw new Exception("Clients did not start");foreach(var handle in plans[owner]){handle.Lock();acquired.Add(handle);}System.Threading.Thread.Sleep(2);}catch(Exception error){lock(state.Mutex)state.Errors.Add(error.Message);}finally{for(int i=acquired.Count-1;i>=0;i--){try{acquired[i].Unlock();}catch(Exception error){lock(state.Mutex)state.Errors.Add(error.Message);}}ResourceState15.Current.Value= -1;}}){IsBackground=true}).ToArray();
  foreach(var thread in threads)thread.Start();valid&=state.Ready.Wait(1000);state.Start.Set();foreach(var thread in threads)valid&=thread.Join(1500);lock(state.Mutex)valid&=state.Errors.Count==0&&state.Owners.All(v=>v== -1);
 }
 return new {actual=new {declarations=admitted.ToArray(),grants=grants.ToArray()},mutationOk=valid};
}
'''
