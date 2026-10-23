#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <memory>
#include <stdexcept>
#include <utility>
struct BankError : std::runtime_error { std::string Code; explicit BankError(std::string code):std::runtime_error(code),Code(std::move(code)){} };
class SetOfStacks {
  int capacity;
  std::vector<std::vector<int>> stacks;

 public:
  SetOfStacks(int supplied) : capacity(supplied) {
    if (supplied < 1 || supplied > 256)
      throw BankError("capacity");
  }
  void Push(int value) {
    int last = static_cast<int>(stacks.size()) - 1;
    if (last < 0 || stacks[last].size() == capacity) {
      stacks.push_back(std::vector<int>());
      ++last;
    }
    stacks[last].push_back(value);
  }
  int Pop() {
    if (static_cast<int>(stacks.size()) == 0)
      throw BankError("empty");
    int last = static_cast<int>(stacks.size()) - 1;
    int value = stacks[last][stacks[last].size() - 1];
    stacks[last].erase(stacks[last].begin() + stacks[last].size() - 1);
    if (stacks[last].size() == 0) {
      stacks.erase(stacks.begin() + last);
    }
    return value;
  }
  int PopAt(int index) {
    if (index < 0 || index >= static_cast<int>(stacks.size()))
      throw BankError("index");
    int value = stacks[index][stacks[index].size() - 1];
    stacks[index].erase(stacks[index].begin() + stacks[index].size() - 1);
    for (int i = index; i + 1 < static_cast<int>(stacks.size()); ++i) {
      int bottom = stacks[i + 1][0];
      stacks[i + 1].erase(stacks[i + 1].begin() + 0);
      stacks[i].push_back(bottom);
    }
    int last = static_cast<int>(stacks.size()) - 1;
    if (stacks[last].size() == 0) {
      stacks.erase(stacks.begin() + last);
    }
    return value;
  }
  bool IsEmpty() {
    return static_cast<int>(stacks.size()) == 0;
  }
};
