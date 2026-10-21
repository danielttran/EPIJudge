#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "binary_tree_node.h"
#include "test_framework/generic_test.h"

// Original EPI Practice algorithm: retain the mathematical target in 64 bits.
namespace {
bool MatchesPath(const BinaryTreeNode<int>* node, std::int64_t remaining) {
  if (!node) return false;
  std::int64_t next_remaining =
      remaining - static_cast<std::int64_t>(node->data);
  if (!node->left && !node->right) return next_remaining == 0;
  return MatchesPath(node->left.get(), next_remaining) ||
         MatchesPath(node->right.get(), next_remaining);
}
}  // namespace
bool HasPathSum(const std::unique_ptr<BinaryTreeNode<int>>& tree,
                int remaining_weight) {
  return MatchesPath(tree.get(), static_cast<std::int64_t>(remaining_weight));
}
int main(int argc, char* argv[]) {
  std::vector<std::string> arguments(argv + 1, argv + argc);
  std::vector<std::string> parameters{"tree", "remaining_weight"};
  return GenericTestMain(arguments, "path_sum.cc", "path_sum.tsv", &HasPathSum,
                         DefaultComparator{}, parameters);
}
