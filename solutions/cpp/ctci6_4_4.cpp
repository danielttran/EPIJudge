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
  bool IsHeightBalanced(TreeNode* root) {
    if (!root)
      return true;
    struct Frame {
      TreeNode* Node;
      bool Exit;
    };
    std::vector<Frame> stack{{root, false}};
    std::unordered_map<TreeNode*, int> heights;
    while (!stack.empty()) {
      auto frame = stack.back();
      stack.pop_back();
      TreeNode* node = frame.Node;
      if (!frame.Exit) {
        stack.push_back({node, true});
        if (node->Right)
          stack.push_back({node->Right, false});
        if (node->Left)
          stack.push_back({node->Left, false});
      } else {
        int left = node->Left ? heights.at(node->Left) : 0,
            right = node->Right ? heights.at(node->Right) : 0;
        if (left - right > 1 || right - left > 1)
          return false;
        heights[node] = 1 + std::max(left, right);
      }
    }
    return true;
  }
};
