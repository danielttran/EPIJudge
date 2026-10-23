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
class TwoStackQueue {
  std::vector<int> newest, oldest;
  void Shift() {
    if (oldest.size() == 0) {
      while (!(newest.size() == 0)) {
        oldest.push_back(newest.back());
        newest.pop_back();
      }
    }
  }

 public:
  TwoStackQueue() = default;
  void Add(int value) {
    newest.push_back(value);
  }
  int Remove() {
    Shift();
    if (oldest.size() == 0)
      throw BankError("empty");
    int value = oldest.back();
    oldest.pop_back();
    return value;
  }
  int Peek() {
    Shift();
    if (oldest.size() == 0)
      throw BankError("empty");
    return oldest.back();
  }
  int Size() {
    return static_cast<int>(newest.size() + oldest.size());
  }
};
