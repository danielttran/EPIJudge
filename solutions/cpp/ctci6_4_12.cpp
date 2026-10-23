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
  int CountDownwardSumPaths(TreeNode* root, int target) {
    if (!root)
      return 0;
    struct Frame {
      TreeNode* Node;
      int Sum;
      bool Exit;
    };
    std::vector<Frame> stack{{root, 0, false}};
    std::unordered_map<int, int> prefix{{0, 1}};
    int answer = 0;
    while (!stack.empty()) {
      auto frame = stack.back();
      stack.pop_back();
      if (frame.Exit) {
        if (--prefix[frame.Sum] == 0)
          prefix.erase(frame.Sum);
        continue;
      }
      int running = frame.Sum + frame.Node->Data;
      auto found = prefix.find(running - target);
      if (found != prefix.end())
        answer += found->second;
      ++prefix[running];
      stack.push_back({frame.Node, running, true});
      if (frame.Node->Right)
        stack.push_back({frame.Node->Right, running, false});
      if (frame.Node->Left)
        stack.push_back({frame.Node->Left, running, false});
    }
    return answer;
  }
};
