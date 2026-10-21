#include <algorithm>
#include <cstddef>
#include <ostream>
#include <stdexcept>
#include <string>
#include <vector>

#include "test_framework/generic_test.h"
#include "test_framework/serialization_traits.h"
#include "test_framework/test_failure.h"

class Queue {
 public:
  explicit Queue(std::size_t capacity)
      : entries_(std::max(std::size_t{1}, capacity)) {}

  explicit Queue(int capacity)
      : Queue(capacity > 0 ? static_cast<std::size_t>(capacity)
                           : std::size_t{1}) {}

  void Enqueue(int value) {
    if (count_ == entries_.size()) {
      std::vector<int> expanded(entries_.size() * 2);
      for (std::size_t index = 0; index < count_; ++index) {
        expanded[index] = entries_[(head_ + index) % entries_.size()];
      }
      entries_.swap(expanded);
      head_ = 0;
    }
    entries_[(head_ + count_) % entries_.size()] = value;
    ++count_;
  }

  int Dequeue() {
    if (count_ == 0) throw std::underflow_error("The queue is empty.");
    const int result = entries_[head_];
    head_ = (head_ + 1) % entries_.size();
    --count_;
    return result;
  }

  int Size() const { return static_cast<int>(count_); }

 private:
  std::vector<int> entries_;
  std::size_t head_ = 0;
  std::size_t count_ = 0;
};

struct QueueOp {
  enum class Operation { kConstruct, kDequeue, kEnqueue, kSize, kUnknown } op;
  int argument;
  std::string name;

  QueueOp(const std::string& operation, int value)
      : argument(value), name(operation) {
    if (name == "Queue")
      op = Operation::kConstruct;
    else if (name == "dequeue")
      op = Operation::kDequeue;
    else if (name == "enqueue")
      op = Operation::kEnqueue;
    else if (name == "size")
      op = Operation::kSize;
    else
      op = Operation::kUnknown;
  }

  void execute(Queue& queue) const {
    switch (op) {
      case Operation::kConstruct:
        queue = Queue(argument);
        break;
      case Operation::kEnqueue:
        queue.Enqueue(argument);
        break;
      case Operation::kDequeue: {
        int actual;
        try {
          actual = queue.Dequeue();
        } catch (const std::underflow_error&) {
          throw TestFailure(
              "A recorded dequeue unexpectedly found the queue empty.");
        }
        if (actual != argument) {
          throw TestFailure(
              "The dequeued value differs from its expected result.")
              .WithProperty(PropertyName::EXPECTED, argument)
              .WithProperty(PropertyName::RESULT, actual);
        }
        break;
      }
      case Operation::kSize: {
        const int actual = queue.Size();
        if (actual != argument) {
          throw TestFailure("The queue size differs from its expected result.")
              .WithProperty(PropertyName::EXPECTED, argument)
              .WithProperty(PropertyName::RESULT, actual);
        }
        break;
      }
      default:
        throw TestFailure("Unknown circular-queue operation: " + name);
    }
  }
};

std::ostream& operator<<(std::ostream& output, const QueueOp& operation) {
  return output << operation.name << '(' << operation.argument << ')';
}

namespace test_framework {
template <>
struct SerializationTrait<QueueOp> : UserSerTrait<QueueOp, std::string, int> {};
}  // namespace test_framework

void QueueTester(const std::vector<QueueOp>& ops) {
  Queue queue(1);
  for (const QueueOp& operation : ops) operation.execute(queue);
}

int main(int argc, char* argv[]) {
  std::vector<std::string> arguments(argv + 1, argv + argc);
  std::vector<std::string> parameters{"ops"};
  return GenericTestMain(arguments, "circular_queue.cc", "circular_queue.tsv",
                         &QueueTester, DefaultComparator{}, parameters);
}
