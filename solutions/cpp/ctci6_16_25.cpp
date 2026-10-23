#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
#include <unordered_map>
#include <unordered_set>
#include <iterator>
#include <list>
#include <optional>
#include <unordered_map>
class LRUCache {
  using Entry = std::pair<int, std::string>;
  int capacity;
  std::list<Entry> order;
  std::unordered_map<int, std::list<Entry>::iterator> index;

 public:
  explicit LRUCache(int capacity) : capacity(capacity) {
  }
  std::optional<std::string> Get(int key) {
    auto found = index.find(key);
    if (found == index.end())
      return std::nullopt;
    order.splice(order.end(), order, found->second);
    return found->second->second;
  }
  void Set(int key, const std::string& value) {
    auto found = index.find(key);
    if (found != index.end()) {
      found->second->second = value;
      order.splice(order.end(), order, found->second);
    } else {
      order.emplace_back(key, value);
      index[key] = std::prev(order.end());
      if (order.size() > static_cast<size_t>(capacity)) {
        index.erase(order.front().first);
        order.pop_front();
      }
    }
  }
};
