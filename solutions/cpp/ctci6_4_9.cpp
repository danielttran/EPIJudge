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
  std::vector<std::vector<int>> BstInsertionSequences(TreeNode* root) {
    std::vector<std::vector<int>> result;
    std::vector<int> path;
    std::function<void(std::vector<TreeNode*>)> visit = [&](std::vector<TreeNode*> available) {
      if (available.empty()) {
        result.push_back(path);
        return;
      }
      for (size_t i = 0; i < available.size(); ++i) {
        auto node = available[i];
        auto following = available;
        following.erase(following.begin() + i);
        if (node->Left)
          following.push_back(node->Left);
        if (node->Right)
          following.push_back(node->Right);
        path.push_back(node->Data);
        visit(std::move(following));
        path.pop_back();
      }
    };
    visit(root ? std::vector<TreeNode*>{root} : std::vector<TreeNode*>{});
    return result;
  }
};
