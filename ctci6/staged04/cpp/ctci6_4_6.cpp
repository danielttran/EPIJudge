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
  TreeNode* InorderSuccessor(TreeNode* node) {
    if (!node)
      return nullptr;
    if (node->Right) {
      auto following = node->Right;
      while (following->Left)
        following = following->Left;
      return following;
    }
    TreeNode* current = node;
    TreeNode* parent = node->Parent;
    while (parent && current == parent->Right) {
      current = parent;
      parent = parent->Parent;
    }
    return parent;
  }
};
