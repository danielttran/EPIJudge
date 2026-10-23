#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
#include <unordered_map>
struct TreeNode {int Data;TreeNode* Left;TreeNode* Right;TreeNode* Parent;explicit TreeNode(int data):Data(data),Left(nullptr),Right(nullptr),Parent(nullptr){}};
class Solution {
 public:
  TreeNode* CreateMinimalBst(const std::vector<int>& sortedValues) {
    std::function<TreeNode*(int, int, TreeNode*)> build = [&](int lower, int upper,
                                                              TreeNode* parent) -> TreeNode* {
      if (lower >= upper)
        return nullptr;
      int middle = lower + (upper - lower) / 2;
      auto node = new TreeNode(sortedValues[middle]);
      node->Parent = parent;
      node->Left = build(lower, middle, node);
      node->Right = build(middle + 1, upper, node);
      return node;
    };
    return build(0, static_cast<int>(sortedValues.size()), nullptr);
  }
};
