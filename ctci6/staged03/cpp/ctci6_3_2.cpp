#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <memory>
#include <stdexcept>
#include <utility>
struct BankError : std::runtime_error { std::string Code; explicit BankError(std::string code):std::runtime_error(code),Code(std::move(code)){} };
class MinStack {
  struct Entry {
    int Value, Minimum;
    std::unique_ptr<Entry> Next;
    Entry(int value, int minimum, std::unique_ptr<Entry> next)
        : Value(value), Minimum(minimum), Next(std::move(next)) {
    }
  };
  std::unique_ptr<Entry> top;

 public:
  MinStack() = default;
  void Push(int value) {
    int minimum = top ? std::min(value, top->Minimum) : value;
    top = std::make_unique<Entry>(value, minimum, std::move(top));
  }
  int Pop() {
    if (!top)
      throw BankError("empty");
    auto removed = std::move(top);
    int value = removed->Value;
    top = std::move(removed->Next);
    return value;
  }
  int Peek() {
    if (!top)
      throw BankError("empty");
    return top->Value;
  }
  int GetMin() {
    if (!top)
      throw BankError("empty");
    return top->Minimum;
  }
  bool IsEmpty() {
    return !top;
  }
};
