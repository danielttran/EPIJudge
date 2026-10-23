"""Native Java threads and shared semaphores, with private work-completion checks."""
CORE=r'''
class OrderState15 {
 final Object mutex=new Object();final java.util.concurrent.Semaphore[] gates={new java.util.concurrent.Semaphore(0),new java.util.concurrent.Semaphore(0)};
 final boolean[] complete=new boolean[3],invoked=new boolean[3];final ArrayList<Integer> events=new ArrayList<>();final ArrayList<String> errors=new ArrayList<>();
 final java.util.concurrent.CountDownLatch ready=new java.util.concurrent.CountDownLatch(3),start=new java.util.concurrent.CountDownLatch(1);
}
class OwnedOrderContext15 extends SyncContext {
 final OrderState15 state;final int role;final Thread owner;int calls;
 OwnedOrderContext15(OrderState15 state,int role){this.state=state;this.role=role;owner=Thread.currentThread();}
 void check(int gate){if(owner!=Thread.currentThread()||++calls>20||gate< -1||gate>1)throw new IllegalStateException("Invalid synchronization API call");}
 public void Wait(int gate){check(gate);try{if(gate<0||!state.gates[gate].tryAcquire(1000,java.util.concurrent.TimeUnit.MILLISECONDS))throw new IllegalStateException("Synchronization did not complete");}catch(InterruptedException error){Thread.currentThread().interrupt();throw new IllegalStateException(error);}}
 public void Signal(int gate){check(gate);if(gate<0)throw new IllegalArgumentException("Invalid gate");state.gates[gate].release();}
 public void Work(){check(-1);synchronized(state.mutex){if(state.invoked[role]||role>0&&!state.complete[role-1])throw new IllegalStateException("Work started before predecessor completion or ran twice");state.invoked[role]=true;state.events.add(role);}try{Thread.sleep(2);}catch(InterruptedException error){Thread.currentThread().interrupt();throw new IllegalStateException(error);}synchronized(state.mutex){state.complete[role]=true;}}
}
'''
INSIDE=r'''
static JsonValue execute(JsonObject row)throws Exception{
 var args=row.get("arguments").asArray();int mask=args.get(1).asInt();var state=new OrderState15();var threads=new ArrayList<Thread>();
 for(var element:args.get(0).asArray()){int role=element.asInt();var thread=new Thread(()->{try{var context=new OwnedOrderContext15(state,role);state.ready.countDown();if(!state.start.await(1000,java.util.concurrent.TimeUnit.MILLISECONDS))throw new IllegalStateException("Workers did not start");if(((mask>>role)&1)!=0)Thread.sleep(4);new Solution_15_5().RunOrdered(role,context);}catch(Throwable error){synchronized(state.mutex){state.errors.add(error.toString());}}});thread.setDaemon(true);threads.add(thread);}
 for(var thread:threads)thread.start();boolean ready=state.ready.await(1000,java.util.concurrent.TimeUnit.MILLISECONDS);state.start.countDown();for(var thread:threads)thread.join(1500);
 synchronized(state.mutex){boolean valid=ready&&state.errors.isEmpty();for(boolean completed:state.complete)valid&=completed;for(var thread:threads)valid&=!thread.isAlive();var actual=new JsonArray();for(int role:state.events)actual.add(role);return new JsonObject().add("actual",actual).add("mutationOk",valid);}
}
'''
