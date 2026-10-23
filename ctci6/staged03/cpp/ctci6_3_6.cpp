#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <memory>
#include <stdexcept>
#include <utility>
struct BankError : std::runtime_error { std::string Code; explicit BankError(std::string code):std::runtime_error(code),Code(std::move(code)){} };
struct Animal { const int Id; const std::string Species; Animal(int id,std::string species):Id(id),Species(std::move(species)){} };
class AnimalShelter {
  struct Entry {
    Animal* Value;
    int Order;
    std::unique_ptr<Entry> Next;
    Entry(Animal* value, int order) : Value(value), Order(order) {
    }
  };
  std::array<std::unique_ptr<Entry>, 2> heads;
  std::array<Entry*, 2> tails{};
  int order = 0, count = 0;
  int Oldest() {
    if (!heads[0])
      return 1;
    if (!heads[1])
      return 0;
    return heads[0]->Order < heads[1]->Order ? 0 : 1;
  }
  Animal* Take(int slot) {
    if (!heads[slot])
      return nullptr;
    auto removed = std::move(heads[slot]);
    Animal* value = removed->Value;
    heads[slot] = std::move(removed->Next);
    if (!heads[slot])
      tails[slot] = nullptr;
    --count;
    return value;
  }

 public:
  AnimalShelter() = default;
  void Enqueue(Animal* animal) {
    int slot;
    if (animal->Species == "dog")
      slot = 0;
    else if (animal->Species == "cat")
      slot = 1;
    else
      throw BankError("species");
    auto entry = std::make_unique<Entry>(animal, order++);
    auto raw = entry.get();
    if (tails[slot])
      tails[slot]->Next = std::move(entry);
    else
      heads[slot] = std::move(entry);
    tails[slot] = raw;
    ++count;
  }
  Animal* DequeueAny() {
    return Take(Oldest());
  }
  Animal* DequeueDog() {
    return Take(0);
  }
  Animal* DequeueCat() {
    return Take(1);
  }
  Animal* Peek() {
    auto& entry = heads[Oldest()];
    return entry ? entry->Value : nullptr;
  }
  int Size() {
    return count;
  }
};
