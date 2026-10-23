"""Real Java philosophers, semaphores and observable exclusive fork ownership."""
CORE=r'''
class DiningState15{
 final Object mutex=new Object();final int n,bites;final java.util.concurrent.Semaphore[] gates;final int[] owners,meals,firstForks;final boolean[] firstAcquired;final java.util.concurrent.CountDownLatch phase=new java.util.concurrent.CountDownLatch(1);final ArrayList<Integer> events=new ArrayList<>();final ArrayList<String> errors=new ArrayList<>();
 final java.util.concurrent.CountDownLatch ready,start=new java.util.concurrent.CountDownLatch(1);
 DiningState15(int n,int bites){this.n=n;this.bites=bites;gates=new java.util.concurrent.Semaphore[n];for(int i=0;i<n;i++)gates[i]=new java.util.concurrent.Semaphore(1);owners=new int[n];Arrays.fill(owners,-1);meals=new int[n];firstForks=new int[n];Arrays.fill(firstForks,-1);firstAcquired=new boolean[n];ready=new java.util.concurrent.CountDownLatch(n);}
 void checkPhase(){for(int r=0;r<n;r++)if(firstForks[r]<0||!firstAcquired[r]&&owners[firstForks[r]]== -1)return;phase.countDown();}
}
class OwnedForkContext15 extends ForkContext{
 final DiningState15 state;final int role;final Thread owner;int calls;
 OwnedForkContext15(DiningState15 state,int role){this.state=state;this.role=role;owner=Thread.currentThread();}
 void check(int fork){if(owner!=Thread.currentThread()||++calls>10000*(state.bites+1)||fork!= -1&&fork!=role&&fork!=(role+1)%state.n)throw new IllegalStateException("Use only owned worker and adjacent fork API");}
 public void Take(int fork){check(fork);boolean first;synchronized(state.mutex){first=state.firstForks[role]<0;if(first)state.firstForks[role]=fork;state.checkPhase();}try{if(fork<0||!state.gates[fork].tryAcquire(1000,java.util.concurrent.TimeUnit.MILLISECONDS))throw new IllegalStateException("Fork acquisition did not complete");synchronized(state.mutex){if(state.owners[fork]!= -1)throw new IllegalStateException("Fork lock was not exclusive");state.owners[fork]=role;if(first)state.firstAcquired[role]=true;state.checkPhase();}if(first&&!state.phase.await(1000,java.util.concurrent.TimeUnit.MILLISECONDS))throw new IllegalStateException("Initial acquisition schedule did not complete");}catch(InterruptedException error){Thread.currentThread().interrupt();throw new IllegalStateException(error);}}
 public void Drop(int fork){check(fork);synchronized(state.mutex){if(fork<0||state.owners[fork]!=role)throw new IllegalStateException("Release only a held fork");state.owners[fork]= -1;}state.gates[fork].release();}
 public void Eat(){check(-1);synchronized(state.mutex){if(state.owners[role]!=role||state.owners[(role+1)%state.n]!=role||state.meals[role]>=state.bites)throw new IllegalStateException("Eat exactly the requested bites while holding both adjacent forks");state.meals[role]++;state.events.add(role);}try{Thread.sleep(2);}catch(InterruptedException error){Thread.currentThread().interrupt();throw new IllegalStateException(error);}}
}
'''
INSIDE=r'''
static JsonValue execute(JsonObject row)throws Exception{var args=row.get("arguments").asArray();int n=args.get(0).asInt(),bites=args.get(1).asInt(),mask=args.get(3).asInt();var state=new DiningState15(n,bites);var threads=new ArrayList<Thread>();
 for(var element:args.get(2).asArray()){int role=element.asInt();var thread=new Thread(()->{try{var context=new OwnedForkContext15(state,role);state.ready.countDown();if(!state.start.await(1000,java.util.concurrent.TimeUnit.MILLISECONDS))throw new IllegalStateException("Workers did not start");if(((mask>>role)&1)!=0)Thread.sleep(4);new Solution_15_3().Dine(role,n,bites,context);}catch(Throwable error){synchronized(state.mutex){state.errors.add(error.toString());}}});thread.setDaemon(true);threads.add(thread);}
 for(var thread:threads)thread.start();boolean ready=state.ready.await(1000,java.util.concurrent.TimeUnit.MILLISECONDS);state.start.countDown();for(var thread:threads)thread.join(1500);
 synchronized(state.mutex){boolean valid=ready&&state.errors.isEmpty();for(int v:state.meals)valid&=v==bites;for(int v:state.owners)valid&=v== -1;for(var thread:threads)valid&=!thread.isAlive();var actual=new JsonArray();for(int role:state.events)actual.add(role);return new JsonObject().add("actual",actual).add("mutationOk",valid);}
}
'''
