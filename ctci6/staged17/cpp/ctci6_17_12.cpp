#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
struct BiNode { int Data; BiNode* Node1=nullptr; BiNode* Node2=nullptr; explicit BiNode(int data):Data(data){} };
class Solution {
 public:
  BiNode* ConvertBiNode(BiNode* root) {
    std::vector<BiNode*> stack;
    BiNode* current = root;
    BiNode* previous = nullptr;
    BiNode* head = nullptr;
    while (current != nullptr || !stack.empty()) {
      while (current != nullptr) {
        stack.push_back(current);
        current = current->Node1;
      }
      BiNode* node = stack.back();
      stack.pop_back();
      BiNode* right = node->Node2;
      node->Node1 = previous;
      if (previous == nullptr)
        head = node;
      else
        previous->Node2 = node;
      previous = node;
      current = right;
    }
    if (previous != nullptr)
      previous->Node2 = nullptr;
    return head;
  }
};
