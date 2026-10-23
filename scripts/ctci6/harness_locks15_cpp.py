"""Borrowed exact lock pointers feed real native clients; graph state is never inspected."""
CORE=r'''
#include <type_traits>
static_assert(std::is_same_v<decltype(std::declval<DeadlockFreeLocks&>().Declare(0,std::declval<const std::vector<int>&>())),bool>,"Declare must return bool");
static_assert(std::is_same_v<decltype(std::declval<DeadlockFreeLocks&>().GetLock(0,0)),ResourceLock*>,"GetLock must return a borrowed ResourceLock pointer");
thread_local int resourceClient15=-1;
struct ResourceState15{
 std::mutex mutex;std::condition_variable changed;std::vector<int> permits,owners;std::array<int,4> firstForks{{-1,-1,-1,-1}};std::array<bool,4> eligible{},firstAcquired{};bool phase=false,start=false;int ready=0;std::vector<std::string> errors;
 explicit ResourceState15(int count):permits(count,1),owners(count,-1){}
 void checkPhase(){for(int r=0;r<4;r++)if(eligible[r]&&(firstForks[r]<0||(!firstAcquired[r]&&owners[firstForks[r]]== -1)))return;phase=true;changed.notify_all();}
};
class NativeResourceLock15:public ResourceLock{
 std::shared_ptr<ResourceState15> state;int resource;
public:
 NativeResourceLock15(std::shared_ptr<ResourceState15> state,int resource):state(std::move(state)),resource(resource){}
 void Lock()override{int role=resourceClient15;if(role<0||role>=4)throw std::runtime_error("Acquire only in registered native clients");std::unique_lock<std::mutex> lock(state->mutex);bool first=state->firstForks[role]<0;if(first)state->firstForks[role]=resource;state->checkPhase();if(!state->changed.wait_for(lock,std::chrono::seconds(1),[&]{return state->permits[resource]>0;}))throw std::runtime_error("Granted lock orders deadlocked");--state->permits[resource];if(state->owners[resource]!= -1)throw std::runtime_error("Native lock was not exclusive");state->owners[resource]=role;if(first)state->firstAcquired[role]=true;state->checkPhase();if(first&&!state->changed.wait_for(lock,std::chrono::seconds(1),[&]{return state->phase;}))throw std::runtime_error("Initial acquisition schedule did not complete");}
 void Unlock()override{int role=resourceClient15;{std::lock_guard<std::mutex> lock(state->mutex);if(role<0||state->owners[resource]!=role)throw std::runtime_error("Release only held native locks");state->owners[resource]= -1;++state->permits[resource];}state->changed.notify_all();}
};
class NativeLockPool15:public LockPool{
 std::vector<std::unique_ptr<NativeResourceLock15>> locks;
public:
 NativeLockPool15(std::shared_ptr<ResourceState15> state,int count){for(int r=0;r<count;r++)locks.push_back(std::make_unique<NativeResourceLock15>(state,r));}
 ResourceLock* Get(int resource)override{if(resource<0||resource>=static_cast<int>(locks.size()))throw std::runtime_error("Invalid pool resource");return locks[resource].get();}
};
json execute(const json& row){
 const auto& args=row["arguments"];int count=args[0].get<int>();auto state=std::make_shared<ResourceState15>(count);NativeLockPool15 pool(state,count);DeadlockFreeLocks factory(count,pool);std::vector<bool> admitted,grants;std::array<std::vector<ResourceLock*>,4> plans;bool valid=true;
 for(const auto& declaration:args[1]){auto values=declaration.get<std::vector<int>>();int owner=values[0];std::vector<int> order(values.begin()+1,values.end()),before=order;bool decision=factory.Declare(owner,order);admitted.push_back(decision);valid&=order==before;std::fill(order.begin(),order.end(),-999);}
 DeadlockFreeLocks other(count,pool);for(int owner=0;owner<4;owner++)for(int resource=0;resource<count;resource++)valid&=other.GetLock(owner,resource)==nullptr;
 for(const auto& request:args[2]){int owner=request[0].get<int>(),resource=request[1].get<int>();ResourceLock* granted=factory.GetLock(owner,resource);grants.push_back(granted!=nullptr);if(granted){if(owner<0||owner>=4||resource<0||resource>=count||granted!=pool.Get(resource))valid=false;else plans[owner].push_back(granted);}}
 bool any=false;for(int owner=0;owner<4;owner++){state->eligible[owner]=!plans[owner].empty();any|=state->eligible[owner];}
 if(valid&&any){std::vector<std::thread> threads;for(int owner=0;owner<4;owner++)threads.emplace_back([state,&plans,owner]{std::vector<ResourceLock*> acquired;resourceClient15=owner;try{{std::unique_lock<std::mutex> lock(state->mutex);++state->ready;state->changed.notify_all();if(!state->changed.wait_for(lock,std::chrono::seconds(1),[&]{return state->start;}))throw std::runtime_error("Clients did not start");}for(auto handle:plans[owner]){handle->Lock();acquired.push_back(handle);}std::this_thread::sleep_for(std::chrono::milliseconds(2));}catch(const std::exception& error){std::lock_guard<std::mutex> lock(state->mutex);state->errors.push_back(error.what());}for(auto it=acquired.rbegin();it!=acquired.rend();++it){try{(*it)->Unlock();}catch(const std::exception& error){std::lock_guard<std::mutex> lock(state->mutex);state->errors.push_back(error.what());}}resourceClient15=-1;});
 {std::unique_lock<std::mutex> lock(state->mutex);valid&=state->changed.wait_for(lock,std::chrono::seconds(1),[&]{return state->ready==4;});state->start=true;}state->changed.notify_all();for(auto& thread:threads)thread.join();valid&=state->errors.empty();for(int owner:state->owners)valid&=owner== -1;
 }
 return json{{"actual",{{"declarations",admitted},{"grants",grants}}},{"mutationOk",valid}};
}
'''
