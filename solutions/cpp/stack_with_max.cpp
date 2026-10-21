#include <algorithm>
#include <stack>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

#include "test_framework/generic_test.h"
#include "test_framework/serialization_traits.h"
#include "test_framework/test_failure.h"

// Original EPI Practice implementation: each depth remembers its prefix
// maximum.
class Stack {
 public:
  void Initialize() { entries_ = std::stack<std::pair<int, int>>{}; }
  bool Empty() const { return entries_.empty(); }
  void Push(int value) {
    int maximum = Empty() ? value : std::max(value, entries_.top().second);
    entries_.push({value, maximum});
  }
  int Pop() {
    if (Empty()) throw std::length_error("empty stack");
    int value = entries_.top().first;
    entries_.pop();
    return value;
  }
  int Max() const {
    if (Empty()) throw std::length_error("empty stack");
    return entries_.top().second;
  }

 private:
  std::stack<std::pair<int, int>> entries_;
};

struct StackOp {
  std::string op;
  int argument;
};
namespace test_framework {
template <>
struct SerializationTrait<StackOp> : UserSerTrait<StackOp, std::string, int> {};
}  // namespace test_framework

void StackTester(const std::vector<StackOp>& operations) {
  Stack state;
  for (const auto& operation : operations) {
    if (operation.op == "Stack")
      state.Initialize();
    else if (operation.op == "push")
      state.Push(operation.argument);
    else if (operation.op == "pop") {
      if (state.Pop() != operation.argument)
        throw TestFailure("Unexpected popped value");
    } else if (operation.op == "max") {
      if (state.Max() != operation.argument)
        throw TestFailure("Unexpected stack maximum");
    } else if (operation.op == "empty") {
      if (state.Empty() != (operation.argument == 1))
        throw TestFailure("Unexpected empty state");
    } else
      throw std::invalid_argument("Unknown stack operation: " + operation.op);
  }
}
int main(int argc, char* argv[]) {
  std::vector<std::string> arguments(argv + 1, argv + argc);
  std::vector<std::string> parameters{"ops"};
  return GenericTestMain(arguments, "stack_with_max.cc", "stack_with_max.tsv",
                         &StackTester, DefaultComparator{}, parameters);
}
