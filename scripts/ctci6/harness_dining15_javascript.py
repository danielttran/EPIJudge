"""Node worker fork mutexes use actual shared-memory permits and role ownership."""
CORE=r'''
const {Worker,isMainThread,workerData,threadId}=require('node:worker_threads');
class OwnedForkContext15 extends ForkContext{
 constructor(shared,role,n,bites){super();this.s=new Int32Array(shared);this.role=role;this.n=n;this.bites=bites;this.owner=threadId;this.calls=0;this.first=true;this.base=3*n+6+n*bites;}
 check(fork=-1){if(threadId!==this.owner||++this.calls>10000*(this.bites+1)||!Number.isInteger(fork)||fork!==-1&&fork!==this.role&&fork!==(this.role+1)%this.n)throw new Error('Use only owned worker and adjacent fork API');}
 phase(){const s=this.s,n=this.n,b=this.base;for(let r=0;r<n;r++){const request=Atomics.load(s,b+r);if(request===0||Atomics.load(s,b+n+r)===0&&Atomics.load(s,n+request-1)===0)return;}Atomics.store(s,b+2*n,1);Atomics.notify(s,b+2*n,n);}
 Take(fork){this.check(fork);if(fork<0)throw new Error('Invalid fork');const s=this.s,first=this.first,deadline=Date.now()+1000;this.first=false;if(first)Atomics.store(s,this.base+this.role,fork+1);this.phase();while(true){const value=Atomics.load(s,fork);if(value>0&&Atomics.compareExchange(s,fork,value,value-1)===value)break;const remaining=deadline-Date.now();if(remaining<=0)throw new Error('Fork acquisition did not complete');Atomics.wait(s,fork,0,remaining);}if(Atomics.compareExchange(s,this.n+fork,0,this.role+1)!==0)throw new Error('Fork lock was not exclusive');if(first)Atomics.store(s,this.base+this.n+this.role,1);this.phase();if(first){const end=Date.now()+1000;while(Atomics.load(s,this.base+2*this.n)===0){const remaining=end-Date.now();if(remaining<=0)throw new Error("Initial acquisition schedule did not complete");Atomics.wait(s,this.base+2*this.n,0,remaining);}}}
 Drop(fork){this.check(fork);if(fork<0||Atomics.compareExchange(this.s,this.n+fork,this.role+1,0)!==this.role+1)throw new Error('Release only a held fork');Atomics.add(this.s,fork,1);Atomics.notify(this.s,fork,1);}
 Eat(){this.check();const s=this.s,n=this.n,r=this.role;if(Atomics.load(s,n+r)!==r+1||Atomics.load(s,n+(r+1)%n)!==r+1||Atomics.add(s,2*n+r,1)>=this.bites)throw new Error('Eat exactly the requested bites while holding both adjacent forks');const index=Atomics.add(s,3*n+4,1);if(index>=n*this.bites)throw new Error('Too many bites');Atomics.store(s,3*n+6+index,r+1);Atomics.wait(s,3*n+5,0,2);}
}
function diningWorker15(){const {n,bites,role,mask,shared}=workerData,s=new Int32Array(shared);try{const context=new OwnedForkContext15(shared,role,n,bites);Atomics.add(s,3*n,1);Atomics.notify(s,3*n);while(Atomics.load(s,3*n+1)===0){if(Atomics.wait(s,3*n+1,0,1000)==='timed-out')throw new Error('Workers did not start');}if((mask>>role)&1)Atomics.wait(s,3*n+5,0,4);if(Dine(role,n,bites,context)!==undefined)throw new Error('Dine must return undefined');}catch(error){Atomics.store(s,3*n+3,1);}finally{Atomics.add(s,3*n+2,1);Atomics.notify(s,3*n+2);}}
function execute(row){
 const [n,bites,order,mask]=row.arguments,shared=new SharedArrayBuffer((5*n+7+n*bites)*4),s=new Int32Array(shared),threads=[];for(let i=0;i<n;++i)s[i]=1;
 for(const role of order){const worker=new Worker(__filename,{workerData:{dining15:true,shared,role,mask,n,bites}});worker.on('error',()=>{Atomics.store(s,3*n+3,1);Atomics.notify(s,3*n);Atomics.notify(s,3*n+2);});threads.push(worker);}
 const waitFor=(index,target)=>{const deadline=Date.now()+3000;while(true){const current=Atomics.load(s,index);if(current>=target)return true;const remaining=deadline-Date.now();if(remaining<=0)return false;Atomics.wait(s,index,current,remaining);}};
 const ready=waitFor(3*n,n);Atomics.store(s,3*n+1,1);Atomics.notify(s,3*n+1,n);const finished=waitFor(3*n+2,n);for(const worker of threads)worker.terminate();
 return {actual:Array.from(s.slice(3*n+6,3*n+6+Math.min(n*bites,Atomics.load(s,3*n+4))),v=>v-1),mutationOk:ready&&finished&&Atomics.load(s,3*n+3)===0&&Array.from({length:n},(_,r)=>Atomics.load(s,n+r)===0&&Atomics.load(s,2*n+r)===bites).every(Boolean)};
}
'''
