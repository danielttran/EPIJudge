"""Native philosopher threads and conditional-permit fork locks with real ownership."""
CORE=r'''
struct DiningState15{
 std::mutex mutex;std::condition_variable changed;int n,bites,ready=0;bool start=false,phase=false;std::vector<int> permits,owners,meals,events,firstForks;std::vector<bool> firstAcquired;std::vector<std::string> errors;
 DiningState15(int n,int bites):n(n),bites(bites),permits(n,1),owners(n,-1),meals(n,0),firstForks(n,-1),firstAcquired(n,false){}
 void checkPhase(){for(int r=0;r<n;r++)if(firstForks[r]<0||(!firstAcquired[r]&&owners[firstForks[r]]== -1))return;phase=true;changed.notify_all();}
};
class OwnedForkContext15:public ForkContext{
 std::shared_ptr<DiningState15> state;int role,calls=0;std::thread::id owner;
 void check(int fork=-1){if(owner!=std::this_thread::get_id()||++calls>10000*(state->bites+1)||(fork!= -1&&fork!=role&&fork!=(role+1)%state->n))throw std::runtime_error("Use only owned worker and adjacent fork API");}
public:
 OwnedForkContext15(std::shared_ptr<DiningState15> state,int role):state(std::move(state)),role(role),owner(std::this_thread::get_id()){}
 void Take(int fork)override{check(fork);if(fork<0)throw std::runtime_error("Invalid fork");{std::unique_lock<std::mutex> lock(state->mutex);bool first=state->firstForks[role]<0;if(first)state->firstForks[role]=fork;state->checkPhase();if(!state->changed.wait_for(lock,std::chrono::seconds(1),[&]{return state->permits[fork]>0;}))throw std::runtime_error("Fork acquisition did not complete");--state->permits[fork];if(state->owners[fork]!= -1)throw std::runtime_error("Fork lock was not exclusive");state->owners[fork]=role;if(first)state->firstAcquired[role]=true;state->checkPhase();if(first&&!state->changed.wait_for(lock,std::chrono::seconds(1),[&]{return state->phase;}))throw std::runtime_error("Initial acquisition schedule did not complete");}}
 void Drop(int fork)override{check(fork);{std::lock_guard<std::mutex> lock(state->mutex);if(fork<0||state->owners[fork]!=role)throw std::runtime_error("Release only a held fork");state->owners[fork]= -1;++state->permits[fork];}state->changed.notify_all();}
 void Eat()override{check();{std::lock_guard<std::mutex> lock(state->mutex);if(state->owners[role]!=role||state->owners[(role+1)%state->n]!=role||state->meals[role]>=state->bites)throw std::runtime_error("Eat exactly the requested bites while holding both adjacent forks");++state->meals[role];state->events.push_back(role);}std::this_thread::sleep_for(std::chrono::milliseconds(2));}
};
json execute(const json& row){
 int n=row["arguments"][0].get<int>(),bites=row["arguments"][1].get<int>(),mask=row["arguments"][3].get<int>();auto order=row["arguments"][2].get<std::vector<int>>();auto state=std::make_shared<DiningState15>(n,bites);std::vector<std::thread> threads;
 for(int role:order)threads.emplace_back([state,role,mask,n,bites]{try{OwnedForkContext15 context(state,role);{std::unique_lock<std::mutex> lock(state->mutex);++state->ready;state->changed.notify_all();if(!state->changed.wait_for(lock,std::chrono::seconds(1),[&]{return state->start;}))throw std::runtime_error("Workers did not start");}if((mask>>role)&1)std::this_thread::sleep_for(std::chrono::milliseconds(4));Solution_15_3().Dine(role,n,bites,context);}catch(const std::exception& error){std::lock_guard<std::mutex> lock(state->mutex);state->errors.push_back(error.what());}});
 bool ready;{std::unique_lock<std::mutex> lock(state->mutex);ready=state->changed.wait_for(lock,std::chrono::seconds(1),[&]{return state->ready==n;});state->start=true;}state->changed.notify_all();for(auto& thread:threads)thread.join();
 bool valid=ready&&state->errors.empty();for(int v:state->meals)valid&=v==bites;for(int v:state->owners)valid&=v== -1;return json{{"actual",state->events},{"mutationOk",valid}};
}
'''
