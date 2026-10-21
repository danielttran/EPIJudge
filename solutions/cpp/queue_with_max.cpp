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
class QueueWithMax {
  std::deque<int> values, maxima;
 public:
  void Enqueue(int value) {
    values.push_back(value);
    while (!maxima.empty() && maxima.back()<value) maxima.pop_back();
    maxima.push_back(value);
  }
  int Dequeue() {
    if (values.empty()) throw std::runtime_error("Empty queue");
    int value=values.front();values.pop_front();
    if (maxima.front()==value) maxima.pop_front();
    return value;
  }
  int Max() const {
    if (values.empty()) throw std::runtime_error("Empty queue");
    return maxima.front();
  }
};
struct QueueOperation { std::string command;int argument; };
namespace test_framework {
template<> struct SerializationTrait<QueueOperation>:UserSerTrait<QueueOperation,std::string,int>{};
}
void VerifyQueue(const std::vector<QueueOperation>& operations) {
  QueueWithMax queue;
  for (const auto& operation:operations) {
    if (operation.command=="QueueWithMax") queue=QueueWithMax{};
    else if (operation.command=="enqueue") queue.Enqueue(operation.argument);
    else if (operation.command=="dequeue") { if (queue.Dequeue()!=operation.argument) throw TestFailure("FIFO result differs"); }
    else if (operation.command=="max") { if (queue.Max()!=operation.argument) throw TestFailure("Maximum differs"); }
    else throw TestFailure("Unsupported operation");
  }
}

int main(int argc, char* argv[]) {
  std::vector<std::string> arguments(argv+1, argv+argc);
  std::vector<std::string> parameters{"ops"};
  return GenericTestMain(arguments,"queue_with_max.cc","queue_with_max.tsv",&VerifyQueue,DefaultComparator{},parameters);
}
