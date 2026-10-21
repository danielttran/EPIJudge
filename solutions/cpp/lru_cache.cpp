#include <cstddef>
#include <list>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

#include "test_framework/generic_test.h"
#include "test_framework/serialization_traits.h"
#include "test_framework/test_failure.h"

// Original EPI Practice implementation: map keys to stable recency-list nodes.
class LruCache {
 public:
  explicit LruCache(std::size_t capacity) : capacity_(capacity) {}
  explicit LruCache(int capacity)
      : capacity_(capacity > 0 ? static_cast<std::size_t>(capacity) : 0) {}
  void Initialize(int capacity) {
    nodes_.clear();
    recency_.clear();
    capacity_ = capacity > 0 ? static_cast<std::size_t>(capacity) : 0;
  }
  int Lookup(int key) {
    auto found = nodes_.find(key);
    if (found == nodes_.end()) return -1;
    recency_.splice(recency_.begin(), recency_, found->second);
    return found->second->second;
  }
  void Insert(int key, int price) {
    auto found = nodes_.find(key);
    if (found != nodes_.end()) {
      recency_.splice(recency_.begin(), recency_, found->second);
      return;  // A repeated insertion refreshes recency but preserves the
               // price.
    }
    if (capacity_ == 0) return;
    if (nodes_.size() == capacity_) {
      nodes_.erase(recency_.back().first);
      recency_.pop_back();
    }
    recency_.push_front({key, price});
    nodes_.emplace(key, recency_.begin());
  }
  bool Erase(int key) {
    auto found = nodes_.find(key);
    if (found == nodes_.end()) return false;
    recency_.erase(found->second);
    nodes_.erase(found);
    return true;
  }

 private:
  std::size_t capacity_;
  std::list<std::pair<int, int>> recency_;
  std::unordered_map<int, std::list<std::pair<int, int>>::iterator> nodes_;
};

struct Op {
  std::string code;
  int arg1;
  int arg2;
};
namespace test_framework {
template <>
struct SerializationTrait<Op> : UserSerTrait<Op, std::string, int, int> {};
}  // namespace test_framework

void LruCacheTester(const std::vector<Op>& operations) {
  LruCache state(0);
  for (const auto& operation : operations) {
    if (operation.code == "LruCache")
      state.Initialize(operation.arg1);
    else if (operation.code == "insert")
      state.Insert(operation.arg1, operation.arg2);
    else if (operation.code == "lookup") {
      if (state.Lookup(operation.arg1) != operation.arg2)
        throw TestFailure("Unexpected cached price");
    } else if (operation.code == "erase") {
      if (state.Erase(operation.arg1) != (operation.arg2 == 1))
        throw TestFailure("Unexpected erase result");
    } else
      throw std::invalid_argument("Unknown cache operation: " + operation.code);
  }
}
int main(int argc, char* argv[]) {
  std::vector<std::string> arguments(argv + 1, argv + argc);
  std::vector<std::string> parameters{"commands"};
  return GenericTestMain(arguments, "lru_cache.cc", "lru_cache.tsv",
                         &LruCacheTester, DefaultComparator{}, parameters);
}
