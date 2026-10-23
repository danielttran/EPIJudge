"""Serialized Java factory methods feed actual shared native locks to concurrent clients."""
CORE=r'''
class ResourceState15{
 static final ThreadLocal<Integer> current=ThreadLocal.withInitial(()-> -1);
 final Object mutex=new Object();final java.util.concurrent.Semaphore[] gates;final int[] owners,firstForks=new int[4];final boolean[] eligible=new boolean[4],firstAcquired=new boolean[4];final ArrayList<String> errors=new ArrayList<>();
 final java.util.concurrent.CountDownLatch phase=new java.util.concurrent.CountDownLatch(1),start=new java.util.concurrent.CountDownLatch(1),ready=new java.util.concurrent.CountDownLatch(4);
 ResourceState15(int count){gates=new java.util.concurrent.Semaphore[count];for(int i=0;i<count;i++)gates[i]=new java.util.concurrent.Semaphore(1);owners=new int[count];Arrays.fill(owners,-1);Arrays.fill(firstForks,-1);}
 void checkPhase(){for(int r=0;r<4;r++)if(eligible[r]&&(firstForks[r]<0||!firstAcquired[r]&&owners[firstForks[r]]== -1))return;phase.countDown();}
}
class NativeResourceLock15 extends ResourceLock{
 final ResourceState15 state;final int resource;
 NativeResourceLock15(ResourceState15 state,int resource){this.state=state;this.resource=resource;}
 public void Lock(){int role=ResourceState15.current.get();if(role<0||role>=4)throw new IllegalStateException("Acquire only in registered native clients");boolean first;synchronized(state.mutex){first=state.firstForks[role]<0;if(first)state.firstForks[role]=resource;state.checkPhase();}try{if(!state.gates[resource].tryAcquire(1000,java.util.concurrent.TimeUnit.MILLISECONDS))throw new IllegalStateException("Granted lock orders deadlocked");synchronized(state.mutex){if(state.owners[resource]!= -1)throw new IllegalStateException("Native lock was not exclusive");state.owners[resource]=role;if(first)state.firstAcquired[role]=true;state.checkPhase();}if(first&&!state.phase.await(1000,java.util.concurrent.TimeUnit.MILLISECONDS))throw new IllegalStateException("Initial acquisition schedule did not complete");}catch(InterruptedException error){Thread.currentThread().interrupt();throw new IllegalStateException(error);}}
 public void Unlock(){int role=ResourceState15.current.get();synchronized(state.mutex){if(role<0||state.owners[resource]!=role)throw new IllegalStateException("Release only held native locks");state.owners[resource]= -1;}state.gates[resource].release();}
}
class NativeLockPool15 extends LockPool{
 final NativeResourceLock15[] locks;
 NativeLockPool15(ResourceState15 state,int count){locks=new NativeResourceLock15[count];for(int r=0;r<count;r++)locks[r]=new NativeResourceLock15(state,r);}
 public ResourceLock Get(int resource){if(resource<0||resource>=locks.length)throw new IllegalArgumentException("Invalid pool resource");return locks[resource];}
}
'''
INSIDE=r'''
static JsonValue execute(JsonObject row)throws Exception{var args=row.get("arguments").asArray();int count=args.get(0).asInt();var state=new ResourceState15(count);var pool=new NativeLockPool15(state,count);var factory=new DeadlockFreeLocks(count,pool);var admitted=new JsonArray();var grants=new JsonArray();var plans=new ArrayList<ArrayList<ResourceLock>>();for(int owner=0;owner<4;owner++)plans.add(new ArrayList<>());boolean valid=true;
 for(var item:args.get(1).asArray()){var declaration=item.asArray();int owner=declaration.get(0).asInt();int[] order=new int[declaration.size()-1];for(int i=0;i<order.length;i++)order[i]=declaration.get(i+1).asInt();int[] before=order.clone();boolean decision=factory.Declare(owner,order);admitted.add(decision);valid&=Arrays.equals(order,before);Arrays.fill(order,-999);}
 var other=new DeadlockFreeLocks(count,pool);for(int owner=0;owner<4;owner++)for(int resource=0;resource<count;resource++)valid&=other.GetLock(owner,resource)==null;
 for(var item:args.get(2).asArray()){var request=item.asArray();int owner=request.get(0).asInt(),resource=request.get(1).asInt();ResourceLock granted=factory.GetLock(owner,resource);grants.add(granted!=null);if(granted!=null){if(owner<0||owner>=4||resource<0||resource>=count||granted!=pool.Get(resource))valid=false;else plans.get(owner).add(granted);}}
 boolean any=false;for(int owner=0;owner<4;owner++){state.eligible[owner]=!plans.get(owner).isEmpty();any|=state.eligible[owner];}
 if(valid&&any){var threads=new ArrayList<Thread>();for(int index=0;index<4;index++){final int owner=index;var thread=new Thread(()->{var acquired=new ArrayList<ResourceLock>();try{ResourceState15.current.set(owner);state.ready.countDown();if(!state.start.await(1000,java.util.concurrent.TimeUnit.MILLISECONDS))throw new IllegalStateException("Clients did not start");for(var handle:plans.get(owner)){handle.Lock();acquired.add(handle);}Thread.sleep(2);}catch(Throwable error){synchronized(state.mutex){state.errors.add(error.toString());}}finally{for(int i=acquired.size()-1;i>=0;i--){try{acquired.get(i).Unlock();}catch(Throwable error){synchronized(state.mutex){state.errors.add(error.toString());}}}ResourceState15.current.remove();}});thread.setDaemon(true);threads.add(thread);}for(var thread:threads)thread.start();valid&=state.ready.await(1000,java.util.concurrent.TimeUnit.MILLISECONDS);state.start.countDown();for(var thread:threads){thread.join(1500);valid&=!thread.isAlive();}synchronized(state.mutex){valid&=state.errors.isEmpty();for(int owner:state.owners)valid&=owner== -1;}}
 return new JsonObject().add("actual",new JsonObject().add("declarations",admitted).add("grants",grants)).add("mutationOk",valid);
}
'''
