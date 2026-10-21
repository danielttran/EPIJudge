#include <stack>
#include <stdexcept>
#include <string>
#include <vector>

#include "test_framework/generic_test.h"
#include "test_framework/serialization_traits.h"
#include "test_framework/test_failure.h"

// Original EPI Practice implementation: reverse an incoming batch only when
// needed.
class Queue {
 public:
  void Initialize() {
    incoming_ = std::stack<int>{};
    outgoing_ = std::stack<int>{};
  }
  void Enqueue(int value) { incoming_.push(value); }
  int Dequeue() {
    if (outgoing_.empty()) {
      while (!incoming_.empty()) {
        outgoing_.push(incoming_.top());
        incoming_.pop();
      }
    }
    if (outgoing_.empty()) throw std::length_error("empty queue");
    int value = outgoing_.top();
    outgoing_.pop();
    return value;
  }

 private:
  std::stack<int> incoming_, outgoing_;
};

struct QueueOp {
  enum class Operation { kConstruct, kDequeue, kEnqueue } op;
  int argument;
  QueueOp(const std::string& name, int value) : argument(value) {
    if (name == "Queue")
      op = Operation::kConstruct;
    else if (name == "dequeue")
      op = Operation::kDequeue;
    else if (name == "enqueue")
      op = Operation::kEnqueue;
    else
      throw std::invalid_argument("Unknown queue operation: " + name);
  }
};
namespace test_framework {
template <>
struct SerializationTrait<QueueOp> : UserSerTrait<QueueOp, std::string, int> {};
}  // namespace test_framework

void QueueTester(const std::vector<QueueOp>& operations) {
  Queue state;
  for (const auto& operation : operations) {
    switch (operation.op) {
      case QueueOp::Operation::kConstruct:
        state.Initialize();
        break;
      case QueueOp::Operation::kEnqueue:
        state.Enqueue(operation.argument);
        break;
      case QueueOp::Operation::kDequeue:
        if (state.Dequeue() != operation.argument)
          throw TestFailure("Unexpected dequeued value");
        break;
      default:
        throw std::invalid_argument("Unknown queue operation");
    }
  }
}
int main(int argc, char* argv[]) {
  std::vector<std::string> arguments(argv + 1, argv + argc);
  std::vector<std::string> parameters{"ops"};
  return GenericTestMain(arguments, "queue_from_stacks.cc",
                         "queue_from_stacks.tsv", &QueueTester,
                         DefaultComparator{}, parameters);
}
