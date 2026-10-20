#include <fstream>
#include <sstream>
#include <unordered_set>
#include <unordered_map>
#include <stdexcept>
#include <chrono>
#include "test_framework/json.h"
using json=nlohmann::json;
#include "solution.cpp"
struct ContractError:std::runtime_error {using std::runtime_error::runtime_error;};
void check(bool ok,const std::string& message="The result violates the problem contract."){if(!ok)throw ContractError(message);}
std::vector<ListNode*> listNodes(ListNode* head){
  std::vector<ListNode*> out;std::unordered_set<ListNode*> seen;
  while(head){check(seen.insert(head).second,"Output list contains a cycle.");out.push_back(head);head=head->next;}return out;
}
std::vector<TreeNode*> treeNodes(TreeNode* root){
  std::vector<TreeNode*> out,q;if(root)q.push_back(root);std::unordered_set<TreeNode*> seen;
  while(!q.empty()){auto n=q.back();q.pop_back();check(seen.insert(n).second,"Tree contains a cycle or shared child.");out.push_back(n);if(n->left)q.push_back(n->left);if(n->right)q.push_back(n->right);}return out;
}
std::vector<Node*> graphNodes(Node* root){
  std::vector<Node*> out,q;if(root)q.push_back(root);std::unordered_set<Node*> seen;
  while(!q.empty()){auto n=q.back();q.pop_back();if(!seen.insert(n).second)continue;out.push_back(n);for(auto c:n->neighbors)q.push_back(c);}return out;
}
ListNode* readList(const json& a){ListNode* head=nullptr;for(auto i=a.rbegin();i!=a.rend();++i)head=new ListNode(i->get<int>(),head);return head;}
std::vector<ListNode*> readLists(const json& a){std::vector<ListNode*> out;for(auto row:a)out.push_back(readList(row));return out;}
TreeNode* readTree(const json& a){
  if(a.empty())return nullptr;auto root=new TreeNode(a[0].get<int>());std::vector<TreeNode*> q{root};size_t i=1;
  for(size_t j=0;j<q.size();j++){auto n=q[j];if(i<a.size()&&!a[i].is_null()){n->left=new TreeNode(a[i].get<int>());q.push_back(n->left);}i++;if(i<a.size()&&!a[i].is_null()){n->right=new TreeNode(a[i].get<int>());q.push_back(n->right);}i++;}return root;
}
Node* readGraph(const json& a){std::vector<Node*> nn;for(size_t i=0;i<a.size();i++)nn.push_back(new Node(static_cast<int>(i+1)));for(size_t i=0;i<nn.size();i++)for(auto c:a[i])nn[i]->neighbors.push_back(nn.at(c.get<int>()-1));return nn.empty()?nullptr:nn[0];}
json dump(ListNode* head){json out=json::array();for(auto n:listNodes(head))out.push_back(n->val);return out;}
json dump(TreeNode* root){
  treeNodes(root);json out=json::array();std::vector<TreeNode*> q;if(root)q.push_back(root);
  for(size_t i=0;i<q.size();i++){auto n=q[i];if(n){out.push_back(n->val);q.push_back(n->left);q.push_back(n->right);}else out.push_back(nullptr);}
  while(!out.empty()&&out.back().is_null())out.erase(out.size()-1);return out;
}
json dump(Node* root){
  auto nn=graphNodes(root);std::sort(nn.begin(),nn.end(),[](auto a,auto b){return a->val<b->val;});json out=json::array();
  for(size_t i=0;i<nn.size();i++){auto n=nn[i];check(n->val==static_cast<int>(i+1),"Graph labels must remain unique and contiguous.");std::vector<int> labels;for(auto c:n->neighbors)labels.push_back(c->val);std::sort(labels.begin(),labels.end());out.push_back(labels);}return out;
}
template<typename T>json dump(const T& value){return json(value);}
// EXECUTE
int main(){
  std::ifstream input("cases.json");json cases;input>>cases;json results=json::array();
  for(auto raw:cases){auto start=std::chrono::steady_clock::now();json actual=nullptr,error=nullptr;bool invalid=false;
    std::ostringstream suppressed;auto output=std::cout.rdbuf(suppressed.rdbuf());
    try{actual=execute(raw);}catch(const ContractError&){invalid=true;}catch(const std::exception& ex){error=ex.what();}catch(...){error="Unknown runtime error.";}
    std::cout.rdbuf(output);
    results.push_back({{"actual",actual},{"error",error},{"validationFailed",invalid},{"elapsedMs",std::chrono::duration<double,std::milli>(std::chrono::steady_clock::now()-start).count()}});
  }std::ofstream report("results.json");report<<results.dump();
}
