"""Factory object identity is checked before marshaling granted native mutex identities to workers."""
CORE=r'''
const {Worker,isMainThread,workerData,threadId}=require('node:worker_threads');
class NativeResourceLock15 extends ResourceLock{
 constructor(resource,shared=null,role=-1,count=0){super();this.resource=resource;this.shared=shared;this.role=role;this.count=count;this.owner=threadId;}
 check(){if(this.shared===null||isMainThread||threadId!==this.owner||this.role<0||this.role>=4)throw new Error('Acquire only in registered native clients');}
 phase(){const s=new Int32Array(this.shared),n=this.count;for(let r=0;r<4;r++){if(Atomics.load(s,2*n+8+r)===0)continue;const request=Atomics.load(s,2*n+r);if(request===0||Atomics.load(s,2*n+4+r)===0&&Atomics.load(s,n+request-1)===0)return;}Atomics.store(s,2*n+12,1);Atomics.notify(s,2*n+12,4);}
 Lock(){this.check();const s=new Int32Array(this.shared),n=this.count,r=this.role,f=this.resource;const first=Atomics.compareExchange(s,2*n+r,0,f+1)===0;this.phase();const deadline=Date.now()+1000;
  while(true){const value=Atomics.load(s,f);if(value>0&&Atomics.compareExchange(s,f,value,value-1)===value)break;const remaining=deadline-Date.now();if(remaining<=0)throw new Error('Granted lock orders deadlocked');Atomics.wait(s,f,0,remaining);}
  if(Atomics.compareExchange(s,n+f,0,r+1)!==0)throw new Error('Native lock was not exclusive');if(first)Atomics.store(s,2*n+4+r,1);this.phase();if(first){const end=Date.now()+1000;while(Atomics.load(s,2*n+12)===0){const remaining=end-Date.now();if(remaining<=0)throw new Error('Initial acquisition schedule did not complete');Atomics.wait(s,2*n+12,0,remaining);}}
 }
 Unlock(){this.check();const s=new Int32Array(this.shared);if(Atomics.compareExchange(s,this.count+this.resource,this.role+1,0)!==this.role+1)throw new Error('Release only held native locks');Atomics.add(s,this.resource,1);Atomics.notify(s,this.resource,1);}
}
class NativeLockPool15 extends LockPool{
 constructor(count){super();this.locks=Array.from({length:count},(_,r)=>new NativeResourceLock15(r));}
 Get(resource){if(!Number.isInteger(resource)||resource<0||resource>=this.locks.length)throw new Error('Invalid pool resource');return this.locks[resource];}
}
function lockClientWorker15(){const {shared,role,count,plan}=workerData,s=new Int32Array(shared),acquired=[];try{Atomics.add(s,2*count+13,1);Atomics.notify(s,2*count+13);while(Atomics.load(s,2*count+14)===0){if(Atomics.wait(s,2*count+14,0,1000)==='timed-out')throw new Error('Clients did not start');}for(const resource of plan){const lock=new NativeResourceLock15(resource,shared,role,count);lock.Lock();acquired.push(lock);}Atomics.wait(s,2*count+17,0,2);}catch(error){Atomics.store(s,2*count+16,1);}finally{for(let i=acquired.length-1;i>=0;--i){try{acquired[i].Unlock();}catch(error){Atomics.store(s,2*count+16,1);}}Atomics.add(s,2*count+15,1);Atomics.notify(s,2*count+15);}}
function execute(row){
 const [count,declarations,requests]=row.arguments,pool=new NativeLockPool15(count),factory=new DeadlockFreeLocks(count,pool),admitted=[],grants=[],plans=Array.from({length:4},()=>[]);let valid=true;
 for(const declaration of declarations){const owner=declaration[0],order=declaration.slice(1),before=JSON.stringify(order),decision=factory.Declare(owner,order);if(typeof decision!=='boolean')throw new Error('Declare must return boolean');admitted.push(decision);valid&&=JSON.stringify(order)===before;order.fill(-999);}
 const other=new DeadlockFreeLocks(count,pool);for(let owner=0;owner<4;++owner)for(let resource=0;resource<count;++resource)valid&&=other.GetLock(owner,resource)===null;
 for(const [owner,resource] of requests){const granted=factory.GetLock(owner,resource);grants.push(granted!==null);if(granted!==null){if(owner<0||owner>=4||resource<0||resource>=count||granted!==pool.Get(resource))valid=false;else plans[owner].push(resource);}}
 if(valid&&plans.some(plan=>plan.length)){
  const shared=new SharedArrayBuffer((2*count+18)*4),s=new Int32Array(shared),threads=[];for(let r=0;r<count;++r)s[r]=1;for(let owner=0;owner<4;++owner)s[2*count+8+owner]=Number(plans[owner].length>0);
  for(let role=0;role<4;++role){const worker=new Worker(__filename,{workerData:{locks15:true,shared,role,count,plan:plans[role]}});worker.on('error',()=>{Atomics.store(s,2*count+16,1);Atomics.notify(s,2*count+13);Atomics.notify(s,2*count+15);});threads.push(worker);}
  const waitFor=(index,target)=>{const deadline=Date.now()+3000;while(true){const current=Atomics.load(s,index);if(current>=target)return true;const remaining=deadline-Date.now();if(remaining<=0)return false;Atomics.wait(s,index,current,remaining);}};
  valid&&=waitFor(2*count+13,4);Atomics.store(s,2*count+14,1);Atomics.notify(s,2*count+14,4);valid&&=waitFor(2*count+15,4);for(const worker of threads)worker.terminate();valid&&=Atomics.load(s,2*count+16)===0&&Array.from({length:count},(_,r)=>Atomics.load(s,count+r)===0).every(Boolean);
 }
 return {actual:{declarations:admitted,grants},mutationOk:valid};
}
'''
