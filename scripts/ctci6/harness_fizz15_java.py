"""Actual Java threads and semaphores; callback verifies exclusive ordered printing."""
CORE=r'''
class FizzState15{
 final Object mutex=new Object();final int limit;final java.util.concurrent.Semaphore[] gates={new java.util.concurrent.Semaphore(1),new java.util.concurrent.Semaphore(0),new java.util.concurrent.Semaphore(0),new java.util.concurrent.Semaphore(0)};
 final ArrayList<String> events=new ArrayList<>(),errors=new ArrayList<>();int next=1;boolean printing;
 final java.util.concurrent.CountDownLatch ready=new java.util.concurrent.CountDownLatch(4),start=new java.util.concurrent.CountDownLatch(1);
 FizzState15(int limit){this.limit=limit;}static int owner(int v){return v%15==0?3:v%3==0?1:v%5==0?2:0;}
}
class OwnedFizzContext15 extends FizzContext{
 final FizzState15 state;final int role;final Thread owner;int calls;
 OwnedFizzContext15(FizzState15 state,int role){this.state=state;this.role=role;owner=Thread.currentThread();}
 void check(int gate){if(owner!=Thread.currentThread()||++calls>4*(state.limit+1)||gate< -1||gate>3)throw new IllegalStateException("Invalid synchronization API call");}
 public void Wait(int gate){check(gate);try{if(gate<0||!state.gates[gate].tryAcquire(1000,java.util.concurrent.TimeUnit.MILLISECONDS))throw new IllegalStateException("Synchronization did not complete");}catch(InterruptedException error){Thread.currentThread().interrupt();throw new IllegalStateException(error);}}
 public void Signal(int gate){check(gate);if(gate<0)throw new IllegalArgumentException("Invalid gate");state.gates[gate].release();}
 public void Print(int value){check(-1);synchronized(state.mutex){if(value<1||value>state.limit||value!=state.next||state.printing||FizzState15.owner(value)!=role)throw new IllegalStateException("Wrong printing role, duplicate, overlap or out-of-order item");state.printing=true;}try{Thread.sleep(2);}catch(InterruptedException error){Thread.currentThread().interrupt();throw new IllegalStateException(error);}synchronized(state.mutex){String text=(value%3==0?"Fizz":"")+(value%5==0?"Buzz":"");state.events.add(text.isEmpty()?Integer.toString(value):text);state.next++;state.printing=false;}}
}
'''
INSIDE=r'''
static JsonValue execute(JsonObject row)throws Exception{if(Solution_15_7.class.getMethod("RunFizzBuzz",int.class,int.class,FizzContext.class).getReturnType()!=void.class)throw new IllegalArgumentException("RunFizzBuzz must return void");var args=row.get("arguments").asArray();int limit=args.get(0).asInt(),mask=args.get(2).asInt();var state=new FizzState15(limit);var threads=new ArrayList<Thread>();
 for(var element:args.get(1).asArray()){int role=element.asInt();var thread=new Thread(()->{try{var context=new OwnedFizzContext15(state,role);state.ready.countDown();if(!state.start.await(1000,java.util.concurrent.TimeUnit.MILLISECONDS))throw new IllegalStateException("Workers did not start");if(((mask>>role)&1)!=0)Thread.sleep(4);new Solution_15_7().RunFizzBuzz(role,limit,context);}catch(Throwable error){synchronized(state.mutex){state.errors.add(error.toString());}}});thread.setDaemon(true);threads.add(thread);}
 for(var thread:threads)thread.start();boolean ready=state.ready.await(1000,java.util.concurrent.TimeUnit.MILLISECONDS);state.start.countDown();for(var thread:threads)thread.join(1500);
 synchronized(state.mutex){boolean valid=ready&&state.errors.isEmpty()&&state.next==limit+1&&!state.printing;for(var thread:threads)valid&=!thread.isAlive();var actual=new JsonArray();for(String text:state.events)actual.add(text);return new JsonObject().add("actual",actual).add("mutationOk",valid);}
}
'''
