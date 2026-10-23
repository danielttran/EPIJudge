#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <memory>
#include <stdexcept>
#include <utility>
struct BankError : std::runtime_error { std::string Code; explicit BankError(std::string code):std::runtime_error(code),Code(std::move(code)){} };
class IntStack {
std::vector<int> values;
public:
void Push(int value) { values.push_back(value); }
int Pop() { if(values.empty()) throw BankError("empty"); int value=values.back(); values.pop_back(); return value; }
int Peek() { if(values.empty()) throw BankError("empty"); return values.back(); }
bool IsEmpty() { return values.empty(); }
};
struct Animal { const int Id; const std::string Species; Animal(int id,std::string species):Id(id),Species(std::move(species)){} };
class ThreeStacks {
  int capacity;
  std::vector<int> values;
  std::array<int, 3> sizes{};
  void Check(int stack) {
    if (stack < 0 || stack >= 3)
      throw BankError("index");
  }

 public:
  ThreeStacks(int supplied) : capacity(supplied) {
    if (supplied < 1 || supplied > 256)
      throw BankError("capacity");
    values.resize(3 * supplied);
  }
  void Push(int stack, int value) {
    Check(stack);
    if (sizes[stack] == capacity)
      throw BankError("full");
    values[stack * capacity + sizes[stack]] = value;
    ++sizes[stack];
  }
  int Pop(int stack) {
    Check(stack);
    if (sizes[stack] == 0)
      throw BankError("empty");
    --sizes[stack];
    return values[stack * capacity + sizes[stack]];
  }
  int Peek(int stack) {
    Check(stack);
    if (sizes[stack] == 0)
      throw BankError("empty");
    return values[stack * capacity + sizes[stack] - 1];
  }
  bool IsEmpty(int stack) {
    Check(stack);
    return sizes[stack] == 0;
  }
  bool IsFull(int stack) {
    Check(stack);
    return sizes[stack] == capacity;
  }
};
