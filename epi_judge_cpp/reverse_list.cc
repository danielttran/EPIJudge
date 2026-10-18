#include "list_node.h"
#include "test_framework/generic_test.h"

shared_ptr<ListNode<int>> ReverseList(const shared_ptr<ListNode<int>>& head) {
  // TODO - you fill in here.
  return nullptr;
}

int main(int argc, char* argv[]) {
  std::vector<std::string> args{argv + 1, argv + argc};
  std::vector<std::string> param_names{"head"};
  return GenericTestMain(args, "reverse_list.cc", "reverse_list.tsv",
                         &ReverseList, DefaultComparator{}, param_names);
}
