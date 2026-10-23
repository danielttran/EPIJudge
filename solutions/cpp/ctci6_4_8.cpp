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
  TreeNode* FirstCommonAncestor(TreeNode* first, TreeNode* second) {
    if (!first || !second)
      return nullptr;
    int depthFirst = 0, depthSecond = 0;
    for (auto cursor = first; cursor; cursor = cursor->Parent)
      ++depthFirst;
    for (auto cursor = second; cursor; cursor = cursor->Parent)
      ++depthSecond;
    while (depthFirst > depthSecond) {
      first = first->Parent;
      --depthFirst;
    }
    while (depthSecond > depthFirst) {
      second = second->Parent;
      --depthSecond;
    }
    while (first != second) {
      first = first->Parent;
      second = second->Parent;
    }
    return first;
  }
};
