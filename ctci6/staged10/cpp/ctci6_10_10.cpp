#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
#include <memory>
class RankTracker {
  struct Node {
    int value, leftCount = 0;
    std::unique_ptr<Node> left, right;
    explicit Node(int value) : value(value) {
    }
  };
  std::unique_ptr<Node> root;

 public:
  RankTracker() = default;
  void Track(int value) {
    if (!root) {
      root = std::make_unique<Node>(value);
      return;
    }
    Node* node = root.get();
    while (true) {
      if (value <= node->value) {
        ++node->leftCount;
        if (!node->left) {
          node->left = std::make_unique<Node>(value);
          return;
        }
        node = node->left.get();
      } else {
        if (!node->right) {
          node->right = std::make_unique<Node>(value);
          return;
        }
        node = node->right.get();
      }
    }
  }
  int GetRank(int value) {
    Node* node = root.get();
    int skipped = 0;
    while (node) {
      if (value == node->value)
        return skipped + node->leftCount;
      if (value < node->value)
        node = node->left.get();
      else {
        skipped += node->leftCount + 1;
        node = node->right.get();
      }
    }
    return -1;
  }
};
