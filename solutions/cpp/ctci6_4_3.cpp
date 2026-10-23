#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
#include <unordered_map>
struct TreeNode {int Data;TreeNode* Left;TreeNode* Right;TreeNode* Parent;explicit TreeNode(int data):Data(data),Left(nullptr),Right(nullptr),Parent(nullptr){}};
struct DepthLink {TreeNode* Value;DepthLink* Next;explicit DepthLink(TreeNode* value):Value(value),Next(nullptr){}};
class Solution {
 public:
  std::vector<DepthLink*> LinkedListsByDepth(TreeNode* root) {
    std::vector<DepthLink*> heads;
    if (!root)
      return heads;
    std::vector<TreeNode*> current{root};
    while (!current.empty()) {
      DepthLink* head = nullptr;
      DepthLink* tail = nullptr;
      std::vector<TreeNode*> following;
      for (auto node : current) {
        auto link = new DepthLink(node);
        if (!tail)
          head = link;
        else
          tail->Next = link;
        tail = link;
        if (node->Left)
          following.push_back(node->Left);
        if (node->Right)
          following.push_back(node->Right);
      }
      heads.push_back(head);
      current = std::move(following);
    }
    return heads;
  }
};
