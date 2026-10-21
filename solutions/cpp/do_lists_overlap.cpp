#include <algorithm>
#include <deque>
#include <functional>
#include <memory>
#include <numeric>
#include <queue>
#include <random>
#include <stdexcept>
#include <string>
#include <tuple>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include "list_node.h"
#include "test_framework/generic_test.h"
#include "test_framework/test_failure.h"
#include "test_framework/timed_executor.h"
#include "test_framework/random_sequence_checker.h"

// Original implementation authored for EPI Practice from its public contract.
std::shared_ptr<ListNode<int>> OverlappingLists(std::shared_ptr<ListNode<int>> first,std::shared_ptr<ListNode<int>> second) {
  std::unordered_set<ListNode<int>*> reachable,seen;
  while (first && reachable.insert(first.get()).second) first=first->next;
  while (second && seen.insert(second.get()).second) {
    if (reachable.count(second.get())) return second;
    second=second->next;
  }
  return nullptr;
}
std::vector<std::shared_ptr<ListNode<int>>> DistinctNodes(std::shared_ptr<ListNode<int>> head) {
  std::vector<std::shared_ptr<ListNode<int>>> result;
  std::unordered_set<ListNode<int>*> seen;
  while (head && seen.insert(head.get()).second) {result.push_back(head);head=head->next;}
  return result;
}
void VerifyOverlap(TimedExecutor& executor,std::shared_ptr<ListNode<int>> first,std::shared_ptr<ListNode<int>> second,std::shared_ptr<ListNode<int>> common,int cycle0,int cycle1) {
  auto Attach=[&](std::shared_ptr<ListNode<int>>& head) {
    if (!head) {head=common;return;}
    auto tail=head;while(tail->next) tail=tail->next;
    tail->next=common;
  };
  Attach(first);Attach(second);
  auto nodes0=DistinctNodes(first),nodes1=DistinctNodes(second);
  if(cycle0>=0 && !nodes0.empty()) nodes0.back()->next=nodes0.at(cycle0);
  if(cycle1>=0 && !nodes1.empty()) nodes1.back()->next=nodes1.at(cycle1);
  auto reachable0=DistinctNodes(first),reachable1=DistinctNodes(second);
  std::unordered_set<ListNode<int>*> left,right;
  std::unordered_map<ListNode<int>*,std::pair<int,ListNode<int>*>> snapshots;
  for(auto node:reachable0) {left.insert(node.get());snapshots[node.get()]={node->data,node->next.get()};}
  for(auto node:reachable1) {right.insert(node.get());snapshots[node.get()]={node->data,node->next.get()};}
  bool overlap=false;for(auto node:left) if(right.count(node)) overlap=true;
  auto result=executor.Run([&]{return OverlappingLists(first,second);});
  if ((overlap && (!result || !left.count(result.get()) || !right.count(result.get()))) || (!overlap && result)) throw TestFailure("Incorrect overlap identity");
  for(auto [node,state]:snapshots) if(node->data!=state.first || node->next.get()!=state.second) throw TestFailure("Input list changed");
}

int main(int argc, char* argv[]) {
  std::vector<std::string> arguments(argv+1, argv+argc);
  std::vector<std::string> parameters{"executor","l0","l1","common","cycle0","cycle1"};
  return GenericTestMain(arguments,"do_lists_overlap.cc","do_lists_overlap.tsv",&VerifyOverlap,DefaultComparator{},parameters);
}
