"""Native std::thread four-role printing with blocking condition-variable permits."""
CORE=r'''
struct FizzState15{
 std::mutex mutex;std::condition_variable changed;int permits[4]={1,0,0,0},ready=0,limit,next=1;bool start=false,printing=false;std::vector<std::string> events,errors;
 explicit FizzState15(int limit):limit(limit){}static int owner(int v){return v%15==0?3:v%3==0?1:v%5==0?2:0;}
};
class OwnedFizzContext15:public FizzContext{
 std::shared_ptr<FizzState15> state;int role,calls=0;std::thread::id owner;
 void check(int gate=-1){if(owner!=std::this_thread::get_id()||++calls>4*(state->limit+1)||gate< -1||gate>3)throw std::runtime_error("Invalid synchronization API call");}
public:
 OwnedFizzContext15(std::shared_ptr<FizzState15> state,int role):state(std::move(state)),role(role),owner(std::this_thread::get_id()){}
 void Wait(int gate)override{check(gate);if(gate<0)throw std::runtime_error("Invalid gate");std::unique_lock<std::mutex> lock(state->mutex);if(!state->changed.wait_for(lock,std::chrono::seconds(1),[&]{return state->permits[gate]>0;}))throw std::runtime_error("Synchronization did not complete");--state->permits[gate];}
 void Signal(int gate)override{check(gate);if(gate<0)throw std::runtime_error("Invalid gate");{std::lock_guard<std::mutex> lock(state->mutex);++state->permits[gate];}state->changed.notify_all();}
 void Print(int value)override{check();{std::lock_guard<std::mutex> lock(state->mutex);if(value<1||value>state->limit||value!=state->next||state->printing||FizzState15::owner(value)!=role)throw std::runtime_error("Wrong printing role, duplicate, overlap or out-of-order item");state->printing=true;}std::this_thread::sleep_for(std::chrono::milliseconds(2));{std::lock_guard<std::mutex> lock(state->mutex);std::string text=(value%3==0?std::string("Fizz"):std::string())+(value%5==0?"Buzz":"");state->events.push_back(text.empty()?std::to_string(value):text);++state->next;state->printing=false;}}
};
json execute(const json& row){
 int limit=row["arguments"][0].get<int>(),mask=row["arguments"][2].get<int>();auto order=row["arguments"][1].get<std::vector<int>>();auto state=std::make_shared<FizzState15>(limit);std::vector<std::thread> threads;
 for(int role:order)threads.emplace_back([state,role,mask,limit]{try{OwnedFizzContext15 context(state,role);{std::unique_lock<std::mutex> lock(state->mutex);++state->ready;state->changed.notify_all();if(!state->changed.wait_for(lock,std::chrono::seconds(1),[&]{return state->start;}))throw std::runtime_error("Workers did not start");}if((mask>>role)&1)std::this_thread::sleep_for(std::chrono::milliseconds(4));Solution_15_7().RunFizzBuzz(role,limit,context);}catch(const std::exception& error){std::lock_guard<std::mutex> lock(state->mutex);state->errors.push_back(error.what());}});
 bool ready;{std::unique_lock<std::mutex> lock(state->mutex);ready=state->changed.wait_for(lock,std::chrono::seconds(1),[&]{return state->ready==4;});state->start=true;}state->changed.notify_all();for(auto& thread:threads)thread.join();return json{{"actual",state->events},{"mutationOk",ready&&state->errors.empty()&&state->next==limit+1&&!state->printing}};
}
'''
