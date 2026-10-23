#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
#include <iterator>
#include <stdexcept>
template <class K, class V>
class HashTable {
  struct Node {
    K key;
    V value;
    Node* next;
    Node(K key, V value, Node* next) : key(std::move(key)), value(std::move(value)), next(next) {
    }
  };
  std::vector<Node*> buckets;
  std::size_t index(const K& key) const {
    return std::hash<K>{}(key) % buckets.size();
  }
  Node* find(const K& key) const {
    for (Node* node = buckets[index(key)]; node; node = node->next)
      if (std::equal_to<K>{}(node->key, key))
        return node;
    return nullptr;
  }

 public:
  explicit HashTable(int capacity) : buckets(capacity, nullptr) {
  }
  HashTable(const HashTable&) = delete;
  HashTable& operator=(const HashTable&) = delete;
  ~HashTable() {
    for (Node* node : buckets)
      while (node) {
        Node* next = node->next;
        delete node;
        node = next;
      }
  }
  void Put(const K& key, const V& value) {
    if (Node* node = find(key)) {
      node->value = value;
      return;
    }
    auto slot = index(key);
    buckets[slot] = new Node(key, value, buckets[slot]);
  }
  V Get(const K& key) const {
    Node* node = find(key);
    if (!node)
      throw std::out_of_range("missing");
    return node->value;
  }
  bool Contains(const K& key) const {
    return find(key) != nullptr;
  }
  bool Remove(const K& key) {
    Node** link = &buckets[index(key)];
    while (*link && !std::equal_to<K>{}((*link)->key, key))
      link = &(*link)->next;
    if (!*link)
      return false;
    Node* removed = *link;
    *link = removed->next;
    delete removed;
    return true;
  }
};
