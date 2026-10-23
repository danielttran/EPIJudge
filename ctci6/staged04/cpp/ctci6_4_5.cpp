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
  bool IsDuplicateLeftBst(TreeNode* root) {
    struct Frame {
      TreeNode* Node;
      long long Lower, Upper;
    };
    std::vector<Frame> stack;
    if (root)
      stack.push_back({root, -2147483649LL, 2147483647LL});
    while (!stack.empty()) {
      auto frame = stack.back();
      stack.pop_back();
      auto node = frame.Node;
      if (node->Data <= frame.Lower || node->Data > frame.Upper)
        return false;
      if (node->Right)
        stack.push_back({node->Right, node->Data, frame.Upper});
      if (node->Left)
        stack.push_back({node->Left, frame.Lower, node->Data});
    }
    return true;
  }
};
