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
class Solution {
 public:
  void SortStack(IntStack& stack) {
    IntStack spare;
    while (!stack.IsEmpty()) {
      int value = stack.Pop();
      while (!spare.IsEmpty() && spare.Peek() > value)
        stack.Push(spare.Pop());
      spare.Push(value);
    }
    while (!spare.IsEmpty())
      stack.Push(spare.Pop());
  }
};
