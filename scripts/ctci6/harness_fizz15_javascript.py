"""Real Node worker isolates with four shared permit gates and a private printer."""
CORE=r'''
const {Worker,isMainThread,workerData,threadId}=require('node:worker_threads');
const fizzOwner15=v=>v%15===0?3:v%3===0?1:v%5===0?2:0;
class OwnedFizzContext15 extends FizzContext{
 constructor(shared,role,limit){super();this.state=new Int32Array(shared);this.role=role;this.limit=limit;this.owner=threadId;this.calls=0;}
 check(gate=-1){if(threadId!==this.owner||++this.calls>4*(this.limit+1)||!Number.isInteger(gate)||gate< -1||gate>3)throw new Error('Invalid synchronization API call');}
 Wait(gate){this.check(gate);if(gate<0)throw new Error('Invalid gate');const deadline=Date.now()+1000;while(true){const value=Atomics.load(this.state,gate);if(value>0&&Atomics.compareExchange(this.state,gate,value,value-1)===value)return;const remaining=deadline-Date.now();if(remaining<=0)throw new Error('Synchronization did not complete');Atomics.wait(this.state,gate,0,remaining);}}
 Signal(gate){this.check(gate);if(gate<0)throw new Error('Invalid gate');Atomics.add(this.state,gate,1);Atomics.notify(this.state,gate,1);}
 Print(value){this.check();const s=this.state;if(!Number.isInteger(value)||value<1||value>this.limit||Atomics.load(s,8)!==value||fizzOwner15(value)!==this.role||Atomics.compareExchange(s,9,0,1)!==0)throw new Error('Wrong printing role, duplicate, overlap or out-of-order item');Atomics.wait(s,15,0,2);Atomics.store(s,16+value-1,value);Atomics.add(s,10,1);Atomics.add(s,8,1);Atomics.store(s,9,0);}
}
function fizzWorker15(){const s=new Int32Array(workerData.shared);try{const context=new OwnedFizzContext15(workerData.shared,workerData.role,workerData.limit);Atomics.add(s,4,1);Atomics.notify(s,4);while(Atomics.load(s,5)===0){if(Atomics.wait(s,5,0,1000)==='timed-out')throw new Error('Workers did not start');}if((workerData.mask>>workerData.role)&1)Atomics.wait(s,15,0,4);if(RunFizzBuzz(workerData.role,workerData.limit,context)!==undefined)throw new Error('RunFizzBuzz must return undefined');}catch(error){Atomics.store(s,7,1);}finally{Atomics.add(s,6,1);Atomics.notify(s,6);}}
function execute(row){
 const [limit,order,mask]=row.arguments,shared=new SharedArrayBuffer((16+limit)*4),s=new Int32Array(shared),threads=[];s[0]=1;s[8]=1;
 for(const role of order){const worker=new Worker(__filename,{workerData:{fizz15:true,shared,role,mask,limit}});worker.on('error',()=>{Atomics.store(s,7,1);Atomics.notify(s,4);Atomics.notify(s,6);});threads.push(worker);}
 const waitFor=(index,target)=>{const deadline=Date.now()+3000;while(true){const current=Atomics.load(s,index);if(current>=target)return true;const remaining=deadline-Date.now();if(remaining<=0)return false;Atomics.wait(s,index,current,remaining);}};
 const ready=waitFor(4,4);Atomics.store(s,5,1);Atomics.notify(s,5,4);const finished=waitFor(6,4);for(const worker of threads)worker.terminate();
 const values=Array.from(s.slice(16,16+Math.min(limit,Atomics.load(s,10))));
 return {actual:values.map(v=>(v%3===0?'Fizz':'')+(v%5===0?'Buzz':'')||String(v)),mutationOk:ready&&finished&&Atomics.load(s,7)===0&&Atomics.load(s,8)===limit+1&&Atomics.load(s,9)===0&&values.length===limit};
}
'''
