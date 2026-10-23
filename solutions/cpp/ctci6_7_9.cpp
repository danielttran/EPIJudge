#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
#include <iterator>
#include <stdexcept>
template <class T>
class CircularArray {
  std::vector<T> items;
  int head = 0;
  void checkIndex(int index) const {
    if (index < 0 || index >= static_cast<int>(items.size()))
      throw std::out_of_range("index");
  }

 public:
  explicit CircularArray(const std::vector<T>& initialValues) : items(initialValues) {
  }
  T Get(int index) const {
    checkIndex(index);
    return items[(head + index) % items.size()];
  }
  void Set(int index, const T& value) {
    checkIndex(index);
    items[(head + index) % items.size()] = value;
  }
  void Rotate(int shift) {
    if (items.empty())
      return;
    int size = static_cast<int>(items.size()), step = shift % size;
    if (step < 0)
      step += size;
    head = (head + step) % size;
  }
  class const_iterator {
    const CircularArray* owner = nullptr;
    std::size_t cursor = 0;

   public:
    using value_type = T;
    using difference_type = std::ptrdiff_t;
    using reference = typename std::vector<T>::const_reference;
    using pointer = void;
    using iterator_category = std::input_iterator_tag;
    const_iterator() = default;
    const_iterator(const CircularArray* owner, std::size_t cursor) : owner(owner), cursor(cursor) {
    }
    reference operator*() const {
      return owner->items[(owner->head + cursor) % owner->items.size()];
    }
    const_iterator& operator++() {
      ++cursor;
      return *this;
    }
    const_iterator operator++(int) {
      auto previous = *this;
      ++*this;
      return previous;
    }
    bool operator==(const const_iterator& other) const {
      return owner == other.owner && cursor == other.cursor;
    }
    bool operator!=(const const_iterator& other) const {
      return !(*this == other);
    }
  };
  const_iterator begin() const {
    return const_iterator(this, 0);
  }
  const_iterator end() const {
    return const_iterator(this, items.size());
  }
};
