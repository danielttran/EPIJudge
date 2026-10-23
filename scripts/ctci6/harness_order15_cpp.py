"""Native std::thread workers; semaphore permits and callback state are private."""
CORE=r'''
#include <type_traits>
static_assert(std::is_same_v<decltype(std::declval<Solution_15_5&>().RunOrdered(0,std::declval<SyncContext&>())),void>,"RunOrdered must return void");
struct OrderState15 {
 std::mutex mutex;std::condition_variable changed;int permits[2]={0,0},ready=0;bool start=false,complete[3]={false,false,false},invoked[3]={false,false,false};std::vector<int> events;std::vector<std::string> errors;
};
class OwnedOrderContext15:public SyncContext {
 std::shared_ptr<OrderState15> state;int role,calls=0;std::thread::id owner;
 void check(int gate=-1){if(owner!=std::this_thread::get_id()||++calls>20||gate< -1||gate>1)throw std::runtime_error("Invalid synchronization API call");}
public:
 OwnedOrderContext15(std::shared_ptr<OrderState15> state,int role):state(std::move(state)),role(role),owner(std::this_thread::get_id()){}
 void Wait(int gate)override{check(gate);if(gate<0)throw std::runtime_error("Invalid gate");std::unique_lock<std::mutex> lock(state->mutex);if(!state->changed.wait_for(lock,std::chrono::seconds(1),[&]{return state->permits[gate]>0;}))throw std::runtime_error("Synchronization did not complete");--state->permits[gate];}
 void Signal(int gate)override{check(gate);if(gate<0)throw std::runtime_error("Invalid gate");{std::lock_guard<std::mutex> lock(state->mutex);++state->permits[gate];}state->changed.notify_all();}
 void Work()override{check();{std::lock_guard<std::mutex> lock(state->mutex);if(state->invoked[role]||(role>0&&!state->complete[role-1]))throw std::runtime_error("Work started before predecessor completion or ran twice");state->invoked[role]=true;state->events.push_back(role);}std::this_thread::sleep_for(std::chrono::milliseconds(2));{std::lock_guard<std::mutex> lock(state->mutex);state->complete[role]=true;}}
};
json execute(const json& row){
 auto order=row["arguments"][0].get<std::vector<int>>();int mask=row["arguments"][1].get<int>();auto state=std::make_shared<OrderState15>();std::vector<std::thread> threads;
 for(int role:order)threads.emplace_back([state,role,mask]{try{OwnedOrderContext15 context(state,role);{std::unique_lock<std::mutex> lock(state->mutex);++state->ready;state->changed.notify_all();if(!state->changed.wait_for(lock,std::chrono::seconds(1),[&]{return state->start;}))throw std::runtime_error("Workers did not start");}if((mask>>role)&1)std::this_thread::sleep_for(std::chrono::milliseconds(4));Solution_15_5().RunOrdered(role,context);}catch(const std::exception& error){std::lock_guard<std::mutex> lock(state->mutex);state->errors.push_back(error.what());}});
 bool ready;{std::unique_lock<std::mutex> lock(state->mutex);ready=state->changed.wait_for(lock,std::chrono::seconds(1),[&]{return state->ready==3;});state->start=true;}state->changed.notify_all();for(auto& thread:threads)thread.join();
 bool valid=ready&&state->errors.empty();for(bool done:state->complete)valid&=done;return json{{"actual",state->events},{"mutationOk",valid}};
}
'''
