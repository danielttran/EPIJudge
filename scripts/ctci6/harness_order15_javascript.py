"""Real Node isolates coordinate via shared-memory Atomics semaphore permits."""
CORE=r'''
const {Worker,isMainThread,workerData,threadId}=require('node:worker_threads');
class OwnedOrderContext15 extends SyncContext{
 constructor(shared,role){super();this.state=new Int32Array(shared);this.role=role;this.owner=threadId;this.calls=0;}
 check(gate=-1){if(threadId!==this.owner||++this.calls>20||!Number.isInteger(gate)||gate< -1||gate>1)throw new Error('Invalid synchronization API call');}
 Wait(gate){this.check(gate);if(gate<0)throw new Error('Invalid gate');const deadline=Date.now()+1000;while(true){const value=Atomics.load(this.state,gate);if(value>0&&Atomics.compareExchange(this.state,gate,value,value-1)===value)return;const remaining=deadline-Date.now();if(remaining<=0)throw new Error('Synchronization did not complete');Atomics.wait(this.state,gate,0,remaining);}}
 Signal(gate){this.check(gate);if(gate<0)throw new Error('Invalid gate');Atomics.add(this.state,gate,1);Atomics.notify(this.state,gate,1);}
 Work(){this.check();const s=this.state,r=this.role;if(Atomics.compareExchange(s,9+r,0,1)!==0||(r>0&&Atomics.load(s,6+r-1)!==1))throw new Error('Work started before predecessor completion or ran twice');const index=Atomics.add(s,16,1);if(index>=3)throw new Error('Duplicate work');Atomics.store(s,13+index,r);Atomics.wait(s,12,0,2);Atomics.store(s,6+r,1);}
}
function orderWorker15(){const s=new Int32Array(workerData.shared);try{const context=new OwnedOrderContext15(workerData.shared,workerData.role);Atomics.add(s,2,1);Atomics.notify(s,2);while(Atomics.load(s,3)===0){if(Atomics.wait(s,3,0,1000)==='timed-out')throw new Error('Workers did not start');}if((workerData.mask>>workerData.role)&1)Atomics.wait(s,12,0,4);if(RunOrdered(workerData.role,context)!==undefined)throw new Error('RunOrdered must return undefined');}catch(error){Atomics.store(s,5,1);}finally{Atomics.add(s,4,1);Atomics.notify(s,4);}}
function execute(row){
 const [order,mask]=row.arguments,shared=new SharedArrayBuffer(17*4),s=new Int32Array(shared),threads=[];
 for(const role of order){const worker=new Worker(__filename,{workerData:{order15:true,shared,role,mask}});worker.on('error',()=>{Atomics.store(s,5,1);Atomics.notify(s,2);Atomics.notify(s,4);});threads.push(worker);}
 const waitFor=(index,target)=>{const deadline=Date.now()+3000;while(true){const current=Atomics.load(s,index);if(current>=target)return true;const remaining=deadline-Date.now();if(remaining<=0)return false;Atomics.wait(s,index,current,remaining);}return true;};
 const ready=waitFor(2,3);Atomics.store(s,3,1);Atomics.notify(s,3,3);const finished=waitFor(4,3);
 for(const worker of threads)worker.terminate();
 return {actual:Array.from(s.slice(13,13+Math.min(3,Atomics.load(s,16)))),mutationOk:ready&&finished&&Atomics.load(s,5)===0&&[0,1,2].every(r=>Atomics.load(s,6+r)===1&&Atomics.load(s,9+r)===1)};
}
'''
