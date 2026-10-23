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
  bool ContainsExactSubtree(TreeNode* large, TreeNode* small) {
    if (!small)
      return true;
    auto encode = [](TreeNode* root) {
      std::vector<std::string> tokens;
      std::vector<TreeNode*> stack{root};
      while (!stack.empty()) {
        auto node = stack.back();
        stack.pop_back();
        if (!node)
          tokens.push_back("#");
        else {
          tokens.push_back("V" + std::to_string(node->Data));
          stack.push_back(node->Right);
          stack.push_back(node->Left);
        }
      }
      return tokens;
    };
    auto text = encode(large), pattern = encode(small);
    std::vector<int> prefix(pattern.size(), 0);
    for (size_t i = 1; i < pattern.size(); ++i) {
      int matched = prefix[i - 1];
      while (matched > 0 && pattern[i] != pattern[matched])
        matched = prefix[matched - 1];
      if (pattern[i] == pattern[matched])
        ++matched;
      prefix[i] = matched;
    }
    int matched = 0;
    for (const auto& token : text) {
      while (matched > 0 && token != pattern[matched])
        matched = prefix[matched - 1];
      if (token == pattern[matched])
        ++matched;
      if (matched == static_cast<int>(pattern.size()))
        return true;
    }
    return false;
  }
};
