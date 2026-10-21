#include <algorithm>
#include <deque>
#include <functional>
#include <memory>
#include <numeric>
#include <queue>
#include <random>
#include <stdexcept>
#include <string>
#include <tuple>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include "list_node.h"
#include "test_framework/generic_test.h"
#include "test_framework/test_failure.h"
#include "test_framework/timed_executor.h"
#include "test_framework/random_sequence_checker.h"

// Original implementation authored for EPI Practice from its public contract.
struct TrafficSample { int time; double volume; };
namespace test_framework {
template<> struct SerializationTrait<TrafficSample>:UserSerTrait<TrafficSample,int,double>{};
}
bool operator==(const TrafficSample& a,const TrafficSample& b) { return a.time==b.time && a.volume==b.volume; }
std::ostream& operator<<(std::ostream& out,const TrafficSample& a) { return out<<a.time<<":"<<a.volume; }
std::vector<TrafficSample> CalculateTrafficVolumes(const std::vector<TrafficSample>& samples,int width) {
  std::deque<int> candidates;
  std::vector<TrafficSample> result;
  for (int index=0;index<static_cast<int>(samples.size());++index) {
    while (!candidates.empty() && static_cast<long long>(samples[index].time)-samples[candidates.front()].time>width) candidates.pop_front();
    while (!candidates.empty() && samples[candidates.back()].volume<=samples[index].volume) candidates.pop_back();
    candidates.push_back(index);
    result.push_back({samples[index].time,samples[candidates.front()].volume});
  }
  return result;
}

int main(int argc, char* argv[]) {
  std::vector<std::string> arguments(argv+1, argv+argc);
  std::vector<std::string> parameters{"A","w"};
  return GenericTestMain(arguments,"max_of_sliding_window.cc","max_of_sliding_window.tsv",&CalculateTrafficVolumes,DefaultComparator{},parameters);
}
