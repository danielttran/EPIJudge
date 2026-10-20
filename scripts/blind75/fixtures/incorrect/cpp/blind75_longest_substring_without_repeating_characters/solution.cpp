#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <queue>
#include <set>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>
struct ListNode { int val; ListNode* next; ListNode(int val=0,ListNode* next=nullptr):val(val),next(next){} };
struct TreeNode { int val; TreeNode *left=nullptr,*right=nullptr; explicit TreeNode(int val=0):val(val){} };
struct Node { int val; std::vector<Node*> neighbors; explicit Node(int val=0):val(val){} };

#include <functional>
#include <sstream>
namespace Probe {
std::vector<ListNode*> nodes(ListNode* n){std::vector<ListNode*>a;while(n){a.push_back(n);n=n->next;}return a;}
ListNode* link(const std::vector<ListNode*>&a){for(size_t i=0;i<a.size();i++)a[i]->next=i+1<a.size()?a[i+1]:nullptr;return a.empty()?nullptr:a[0];}
TreeNode* invert(TreeNode* n){if(n){auto l=invert(n->left);n->left=invert(n->right);n->right=l;}return n;}
int depth(TreeNode*n){return n?1+std::max(depth(n->left),depth(n->right)):0;}
bool same(TreeNode*a,TreeNode*b){return !a||!b?a==b:a->val==b->val&&same(a->left,b->left)&&same(a->right,b->right);}
bool subtree(TreeNode*a,TreeNode*b){return !b||(a&&(same(a,b)||subtree(a->left,b)||subtree(a->right,b)));}
std::vector<std::vector<int>> levels(TreeNode*root){std::vector<std::vector<int>>out;std::vector<TreeNode*>q;if(root)q.push_back(root);while(!q.empty()){std::vector<int>row;std::vector<TreeNode*>next;for(auto n:q){row.push_back(n->val);if(n->left)next.push_back(n->left);if(n->right)next.push_back(n->right);}out.push_back(row);q=next;}return out;}
TreeNode* build(std::vector<int>pre,std::vector<int>ino){if(pre.empty())return nullptr;auto i=std::find(ino.begin(),ino.end(),pre[0])-ino.begin();auto n=new TreeNode(pre[0]);n->left=build({pre.begin()+1,pre.begin()+i+1},{ino.begin(),ino.begin()+i});n->right=build({pre.begin()+i+1,pre.end()},{ino.begin()+i+1,ino.end()});return n;}
std::vector<int> inorder(TreeNode*n){if(!n)return {};auto a=inorder(n->left);a.push_back(n->val);auto b=inorder(n->right);a.insert(a.end(),b.begin(),b.end());return a;}
int gain(TreeNode*n,int&best){if(!n)return 0;int l=std::max(0,gain(n->left,best)),r=std::max(0,gain(n->right,best));best=std::max(best,n->val+l+r);return n->val+std::max(l,r);}
int maxPath(TreeNode*n){int best=INT32_MIN;gain(n,best);return best;}
std::string serialize(TreeNode*n){return n?std::to_string(n->val)+" "+serialize(n->left)+serialize(n->right):"# ";}
TreeNode* read(std::istringstream&in){std::string s;in>>s;if(s=="#")return nullptr;auto n=new TreeNode(std::stoi(s));n->left=read(in);n->right=read(in);return n;}
TreeNode* deserialize(const std::string&s){std::istringstream in(s);return read(in);}
Node* copy(Node*n,std::unordered_map<Node*,Node*>&copies){if(!n)return nullptr;if(copies.count(n))return copies[n];auto c=new Node(n->val);copies[n]=c;for(auto next:n->neighbors)c->neighbors.push_back(copy(next,copies));return c;}
Node* clone(Node*n){std::unordered_map<Node*,Node*>copies;return copy(n,copies);}
}

class Solution {
int ActualCorrect(std::string s){
std::array<int,128>last;last.fill(-1);int left=0,best=0;for(int i=0;i<static_cast<int>(s.size());i++){auto c=static_cast<unsigned char>(s[i]);left=std::max(left,last[c]+1);last[c]=i;best=std::max(best,i-left+1);}return best;
}

public:
int LengthOfLongestSubstring(std::string s) {
auto value=ActualCorrect(s);
return value ^ 1;
}
};
