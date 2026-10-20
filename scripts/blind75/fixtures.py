"""Generate actual test-only algorithms and deliberate contract violations.

Every positive fixture computes its answer without reading expected outputs.
Python ordinary-function fixtures execute the independent mathematical oracle.
"""
import json
from algorithms import body as ordinary_body
from negative import make as negative_fixture
from generate import ROOT, LANGS, STATE, starter

CSPROBE=r'''
public static class Probe {
  public static List<ListNode> Nodes(ListNode? n){var a=new List<ListNode>();while(n!=null){a.Add(n);n=n.next;}return a;}
  public static ListNode? Link(IEnumerable<ListNode> sequence){var a=sequence.ToArray();for(int i=0;i<a.Length;i++)a[i].next=i+1<a.Length?a[i+1]:null;return a.FirstOrDefault();}
  public static TreeNode? Invert(TreeNode? n){if(n!=null){var l=Invert(n.left);n.left=Invert(n.right);n.right=l;}return n;}
  public static int Depth(TreeNode? n)=>n==null?0:1+Math.Max(Depth(n.left),Depth(n.right));
  public static bool Same(TreeNode? a,TreeNode? b)=>a==null||b==null?a==b:a.val==b.val&&Same(a.left,b.left)&&Same(a.right,b.right);
  public static bool Subtree(TreeNode? a,TreeNode? b)=>b==null||a!=null&&(Same(a,b)||Subtree(a.left,b)||Subtree(a.right,b));
  public static int[][] Levels(TreeNode? root){var result=new List<int[]>();var q=new List<TreeNode>();if(root!=null)q.Add(root);while(q.Count>0){result.Add(q.Select(n=>n.val).ToArray());q=q.SelectMany(n=>new[]{n.left,n.right}).OfType<TreeNode>().ToList();}return result.ToArray();}
  public static TreeNode? Build(int[] pre,int[] ino){if(pre.Length==0)return null;int i=Array.IndexOf(ino,pre[0]);return new TreeNode(pre[0],Build(pre[1..(i+1)],ino[..i]),Build(pre[(i+1)..],ino[(i+1)..]));}
  public static IEnumerable<int> Inorder(TreeNode? n)=>n==null?Enumerable.Empty<int>():Inorder(n.left).Concat(new[]{n.val}).Concat(Inorder(n.right));
  public static int MaxPath(TreeNode root){int best=int.MinValue;int Gain(TreeNode? n){if(n==null)return 0;int l=Math.Max(0,Gain(n.left)),r=Math.Max(0,Gain(n.right));best=Math.Max(best,n.val+l+r);return n.val+Math.Max(l,r);}Gain(root);return best;}
  public static string Serialize(TreeNode? n)=>n==null?"# ":n.val+" "+Serialize(n.left)+Serialize(n.right);
  public static TreeNode? Deserialize(string text){var q=new Queue<string>(text.Split(' ',StringSplitOptions.RemoveEmptyEntries));TreeNode? Read(){string s=q.Dequeue();return s=="#"?null:new TreeNode(int.Parse(s),Read(),Read());}return Read();}
  public static Node? Clone(Node? root){var copies=new Dictionary<Node,Node>();Node? Copy(Node? n){if(n==null)return null;if(copies.TryGetValue(n,out var c))return c;c=new Node(n.val);copies[n]=c;c.neighbors=n.neighbors.Select(x=>Copy(x)!).ToList();return c;}return Copy(root);}
}
'''
JAVAPROBE=r'''
class Probe {
  static List<ListNode> nodes(ListNode n){List<ListNode>a=new ArrayList<>();while(n!=null){a.add(n);n=n.next;}return a;}
  static ListNode link(List<ListNode>a){for(int i=0;i<a.size();i++)a.get(i).next=i+1<a.size()?a.get(i+1):null;return a.isEmpty()?null:a.get(0);}
  static TreeNode invert(TreeNode n){if(n!=null){TreeNode l=invert(n.left);n.left=invert(n.right);n.right=l;}return n;}
  static int depth(TreeNode n){return n==null?0:1+Math.max(depth(n.left),depth(n.right));}
  static boolean same(TreeNode a,TreeNode b){return a==null||b==null?a==b:a.val==b.val&&same(a.left,b.left)&&same(a.right,b.right);}
  static boolean subtree(TreeNode a,TreeNode b){return b==null||a!=null&&(same(a,b)||subtree(a.left,b)||subtree(a.right,b));}
  static int[][] levels(TreeNode root){List<int[]>out=new ArrayList<>();List<TreeNode>q=new ArrayList<>();if(root!=null)q.add(root);while(!q.isEmpty()){out.add(q.stream().mapToInt(n->n.val).toArray());List<TreeNode>next=new ArrayList<>();for(TreeNode n:q){if(n.left!=null)next.add(n.left);if(n.right!=null)next.add(n.right);}q=next;}return out.toArray(int[][]::new);}
  static TreeNode build(int[]pre,int[]ino){if(pre.length==0)return null;int i=0;while(ino[i]!=pre[0])i++;TreeNode n=new TreeNode(pre[0]);n.left=build(Arrays.copyOfRange(pre,1,i+1),Arrays.copyOfRange(ino,0,i));n.right=build(Arrays.copyOfRange(pre,i+1,pre.length),Arrays.copyOfRange(ino,i+1,ino.length));return n;}
  static List<Integer> inorder(TreeNode n){List<Integer>out=new ArrayList<>();if(n!=null){out.addAll(inorder(n.left));out.add(n.val);out.addAll(inorder(n.right));}return out;}
  static int gain(TreeNode n,int[]best){if(n==null)return 0;int l=Math.max(0,gain(n.left,best)),r=Math.max(0,gain(n.right,best));best[0]=Math.max(best[0],n.val+l+r);return n.val+Math.max(l,r);}
  static int maxPath(TreeNode n){int[]best={Integer.MIN_VALUE};gain(n,best);return best[0];}
  static String serialize(TreeNode n){return n==null?"# ":n.val+" "+serialize(n.left)+serialize(n.right);}
  static TreeNode read(Deque<String>q){String s=q.remove();if(s.equals("#"))return null;TreeNode n=new TreeNode(Integer.parseInt(s));n.left=read(q);n.right=read(q);return n;}
  static TreeNode deserialize(String s){return read(new ArrayDeque<>(Arrays.asList(s.trim().split(" +"))));}
  static Node clone(Node root){return clone(root,new IdentityHashMap<>());}
  static Node clone(Node n,IdentityHashMap<Node,Node>copies){if(n==null)return null;if(copies.containsKey(n))return copies.get(n);Node c=new Node(n.val);copies.put(n,c);for(Node next:n.neighbors)c.neighbors.add(clone(next,copies));return c;}
}
'''
CPPPROBE=r'''
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
'''
JSPROBE=r'''
const Probe={
 nodes(n){const a=[];while(n){a.push(n);n=n.next;}return a;},
 link(a){a.forEach((n,i)=>n.next=a[i+1]??null);return a[0]??null;},
 invert(n){if(n){const l=this.invert(n.left);n.left=this.invert(n.right);n.right=l;}return n;},
 depth(n){return n?1+Math.max(this.depth(n.left),this.depth(n.right)):0;},
 same(a,b){return !a||!b?a===b:a.val===b.val&&this.same(a.left,b.left)&&this.same(a.right,b.right);},
 subtree(a,b){return !b||!!a&&(this.same(a,b)||this.subtree(a.left,b)||this.subtree(a.right,b));},
 levels(root){const out=[];let q=root?[root]:[];while(q.length){out.push(q.map(n=>n.val));q=q.flatMap(n=>[n.left,n.right].filter(Boolean));}return out;},
 build(pre,ino){if(!pre.length)return null;const i=ino.indexOf(pre[0]);return new TreeNode(pre[0],this.build(pre.slice(1,i+1),ino.slice(0,i)),this.build(pre.slice(i+1),ino.slice(i+1)));},
 inorder(n){return n?[...this.inorder(n.left),n.val,...this.inorder(n.right)]:[];},
 maxPath(root){let best=-Infinity;function gain(n){if(!n)return 0;const l=Math.max(0,gain(n.left)),r=Math.max(0,gain(n.right));best=Math.max(best,n.val+l+r);return n.val+Math.max(l,r);}gain(root);return best;},
 serialize(n){return n?n.val+' '+this.serialize(n.left)+this.serialize(n.right):'# ';},
 deserialize(s){const a=s.trim().split(/ +/);let i=0;function read(){const s=a[i++];return s==='#'?null:new TreeNode(Number(s),read(),read());}return read();},
 clone(root){const copies=new Map();function copy(n){if(!n)return null;if(copies.has(n))return copies.get(n);const c=new Node(n.val);copies.set(n,c);c.neighbors=n.neighbors.map(copy);return c;}return copy(root);}
};
'''
PYPROBE=r'''
class Probe:
    @staticmethod
    def nodes(n):
        out=[]
        while n is not None: out.append(n); n=n.next
        return out
    @staticmethod
    def link(a):
        for i,n in enumerate(a): n.next=a[i+1] if i+1<len(a) else None
        return a[0] if a else None
    @staticmethod
    def invert(n):
        if n: n.left,n.right=Probe.invert(n.right),Probe.invert(n.left)
        return n
    @staticmethod
    def depth(n): return 1+max(Probe.depth(n.left),Probe.depth(n.right)) if n else 0
    @staticmethod
    def same(a,b): return a is b if a is None or b is None else a.val==b.val and Probe.same(a.left,b.left) and Probe.same(a.right,b.right)
    @staticmethod
    def subtree(a,b): return b is None or a is not None and (Probe.same(a,b) or Probe.subtree(a.left,b) or Probe.subtree(a.right,b))
    @staticmethod
    def levels(root):
        out=[];q=[root] if root else []
        while q: out.append([n.val for n in q]); q=[c for n in q for c in [n.left,n.right] if c]
        return out
    @staticmethod
    def build(pre,ino):
        if not pre: return None
        i=ino.index(pre[0]);return TreeNode(pre[0],Probe.build(pre[1:i+1],ino[:i]),Probe.build(pre[i+1:],ino[i+1:]))
    @staticmethod
    def inorder(n): return Probe.inorder(n.left)+[n.val]+Probe.inorder(n.right) if n else []
    @staticmethod
    def max_path(root):
        best=-10**30
        def gain(n):
            nonlocal best
            if not n: return 0
            l=max(0,gain(n.left));r=max(0,gain(n.right));best=max(best,n.val+l+r);return n.val+max(l,r)
        gain(root);return best
    @staticmethod
    def serialize(n): return str(n.val)+' '+Probe.serialize(n.left)+Probe.serialize(n.right) if n else '# '
    @staticmethod
    def deserialize(s):
        tokens=iter(s.split())
        def read():
            token=next(tokens)
            return None if token=='#' else TreeNode(int(token),read(),read())
        return read()
    @staticmethod
    def clone(root):
        copies={}
        def copy(n):
            if n is None:return None
            if n in copies:return copies[n]
            c=Node(n.val);copies[n]=c;c.neighbors=[copy(v) for v in n.neighbors];return c
        return copy(root)
'''
PROBES=dict(csharp=CSPROBE,java=JAVAPROBE,cpp=CPPPROBE,javascript=JSPROBE,python=PYPROBE)

# Helpers must precede C++ inline methods; other languages resolve later definitions.
def bodymap(s,lang):
    m=s['method'];mode=s['mode'];cs=lang=='csharp';cpp=lang=='cpp';py=lang=='python'
    def select(*values):return values[LANGS.index(lang)]
    def ret(expr):return 'return '+expr+('' if py else ';')
    args=[p['name'] for p in s['params']]
    probe_names={'MaxDepth':('Depth','depth'),'IsSameTree':('Same','same'),'IsSubtree':('Subtree','subtree'),'LevelOrder':('Levels','levels'),'BuildTree':('Build','build'),'MaxPathSum':('MaxPath','maxPath'),'InvertTree':('Invert','invert'),'CloneGraph':('Clone','clone')}
    if m in probe_names:
        fn=probe_names[m][0 if cs else 1]
        if py and fn=='maxPath':fn='max_path'
        return {m:ret('Probe'+('::' if cpp else '.')+fn+'('+', '.join(args)+')')}
    if m=='IsValidBST':return {m:select('var a=Probe.Inorder(root).ToArray();return a.Zip(a.Skip(1)).All(p=>p.First<p.Second);','const a=Probe.inorder(root);return a.every((v,i)=>i===0||a[i-1]<v);','a=Probe.inorder(root)\nreturn all(a[i-1]<a[i] for i in range(1,len(a)))','auto a=Probe::inorder(root);for(size_t i=1;i<a.size();i++)if(a[i-1]>=a[i])return false;return true;','List<Integer>a=Probe.inorder(root);for(int i=1;i<a.size();i++)if(a.get(i-1)>=a.get(i))return false;return true;')}
    if m=='KthSmallest':return {m:ret(select('Probe.Inorder(root).ElementAt(k-1)','Probe.inorder(root)[k-1]','Probe.inorder(root)[k-1]','Probe::inorder(root).at(k-1)','Probe.inorder(root).get(k-1)'))}
    if m=='LowestCommonAncestor':return {m:select('while(root!=null){if(p<root.val&&q<root.val)root=root.left;else if(p>root.val&&q>root.val)root=root.right;else return root;}return null;','while(root){if(p<root.val&&q<root.val)root=root.left;else if(p>root.val&&q>root.val)root=root.right;else return root;}return null;','while root:\n    if max(p,q)<root.val:root=root.left\n    elif min(p,q)>root.val:root=root.right\n    else:return root\nreturn None','while(root){if(p<root->val&&q<root->val)root=root->left;else if(p>root->val&&q>root->val)root=root->right;else return root;}return nullptr;','while(root!=null){if(p<root.val&&q<root.val)root=root.left;else if(p>root.val&&q>root.val)root=root.right;else return root;}return null;')}
    if m=='HasCycle':return {m:select('var slow=head;var fast=head;while(fast?.next!=null){slow=slow!.next;fast=fast.next.next;if(ReferenceEquals(slow,fast))return true;}return false;','let slow=head,fast=head;while(fast&&fast.next){slow=slow.next;fast=fast.next.next;if(slow===fast)return true;}return false;','slow=fast=head\nwhile fast and fast.next:\n    slow=slow.next;fast=fast.next.next\n    if slow is fast:return True\nreturn False','auto slow=head,fast=head;while(fast&&fast->next){slow=slow->next;fast=fast->next->next;if(slow==fast)return true;}return false;','ListNode slow=head,fast=head;while(fast!=null&&fast.next!=null){slow=slow.next;fast=fast.next.next;if(slow==fast)return true;}return false;')}
    if mode in ('list_reuse','list_reorder','list_remove'):
        init=select('var a=Probe.Nodes(head);','let a=Probe.nodes(head);','a=Probe.nodes(head)','auto a=Probe::nodes(head);','List<ListNode>a=Probe.nodes(head);')
        if m=='MergeTwoLists':init=select('var a=Probe.Nodes(list1).Concat(Probe.Nodes(list2)).OrderBy(n=>n.val).ToList();','let a=[...Probe.nodes(list1),...Probe.nodes(list2)].sort((a,b)=>a.val-b.val);','a=sorted(Probe.nodes(list1)+Probe.nodes(list2),key=lambda n:n.val)','auto a=Probe::nodes(list1);auto b=Probe::nodes(list2);a.insert(a.end(),b.begin(),b.end());std::stable_sort(a.begin(),a.end(),[](auto x,auto y){return x->val<y->val;});','List<ListNode>a=Probe.nodes(list1);a.addAll(Probe.nodes(list2));a.sort(Comparator.comparingInt(n->n.val));')
        if m=='MergeKLists':init=select('var a=lists.SelectMany(Probe.Nodes).OrderBy(n=>n.val).ToList();','let a=lists.flatMap(Probe.nodes).sort((a,b)=>a.val-b.val);','a=sorted([n for h in lists for n in Probe.nodes(h)],key=lambda n:n.val)','std::vector<ListNode*>a;for(auto h:lists){auto b=Probe::nodes(h);a.insert(a.end(),b.begin(),b.end());}std::stable_sort(a.begin(),a.end(),[](auto x,auto y){return x->val<y->val;});','List<ListNode>a=new ArrayList<>();for(ListNode h:lists)a.addAll(Probe.nodes(h));a.sort(Comparator.comparingInt(n->n.val));')
        operation=''
        if m=='ReverseList':operation=select('a.Reverse();','a.reverse();','a.reverse()','std::reverse(a.begin(),a.end());','Collections.reverse(a);')
        if m=='RemoveNthFromEnd':operation=select('a.RemoveAt(a.Count-n);','a.splice(a.length-n,1);','a.pop(len(a)-n)','a.erase(a.end()-n);','a.remove(a.size()-n);')
        if m=='ReorderList':operation=select('var b=new List<ListNode>();for(int i=0,j=a.Count-1;i<=j;i++,j--){b.Add(a[i]);if(i<j)b.Add(a[j]);}a=b;','const b=[];for(let i=0,j=a.length-1;i<=j;i++,j--){b.push(a[i]);if(i<j)b.push(a[j]);}a=b;','b=[]\nfor i in range((len(a)+1)//2):\n    b.append(a[i])\n    if i!=len(a)-1-i:b.append(a[-1-i])\na=b','std::vector<ListNode*>b;for(int i=0,j=static_cast<int>(a.size())-1;i<=j;i++,j--){b.push_back(a[i]);if(i<j)b.push_back(a[j]);}a=b;','List<ListNode>b=new ArrayList<>();for(int i=0,j=a.size()-1;i<=j;i++,j--){b.add(a.get(i));if(i<j)b.add(a.get(j));}a=b;')
        link=select('Probe.Link(a)','Probe.link(a)','Probe.link(a)','Probe::link(a)','Probe.link(a)')
        return {m:init+'\n'+operation+'\n'+(link+('' if py else ';') if mode=='list_reorder' else ret(link))}
    if mode=='matrix_inplace':
        if m=='Rotate':return {m:select('var copy=matrix.Select(r=>r.ToArray()).ToArray();int n=matrix.Length;for(int r=0;r<n;r++)for(int c=0;c<n;c++)matrix[r][c]=copy[n-1-c][r];','const copy=matrix.map(r=>[...r]),n=matrix.length;for(let r=0;r<n;r++)for(let c=0;c<n;c++)matrix[r][c]=copy[n-1-c][r];','copy=[row[:] for row in matrix];n=len(matrix)\nfor r in range(n):\n    for c in range(n):matrix[r][c]=copy[n-1-c][r]','auto copy=matrix;int n=static_cast<int>(matrix.size());for(int r=0;r<n;r++)for(int c=0;c<n;c++)matrix[r][c]=copy[n-1-c][r];','int[][]copy=Arrays.stream(matrix).map(int[]::clone).toArray(int[][]::new);int n=matrix.length;for(int r=0;r<n;r++)for(int c=0;c<n;c++)matrix[r][c]=copy[n-1-c][r];')}
        return {m:select('var copy=matrix.Select(r=>r.ToArray()).ToArray();for(int r=0;r<matrix.Length;r++)for(int c=0;c<matrix[r].Length;c++)if(copy[r].Contains(0)||copy.Any(row=>row[c]==0))matrix[r][c]=0;','const copy=matrix.map(r=>[...r]);for(let r=0;r<matrix.length;r++)for(let c=0;c<matrix[r].length;c++)if(copy[r].includes(0)||copy.some(row=>row[c]===0))matrix[r][c]=0;','copy=[row[:] for row in matrix]\nfor r in range(len(matrix)):\n    for c in range(len(matrix[r])):\n        if 0 in copy[r] or any(row[c]==0 for row in copy):matrix[r][c]=0','auto copy=matrix;for(size_t r=0;r<matrix.size();r++)for(size_t c=0;c<matrix[r].size();c++){bool zero=false;for(auto v:copy[r])zero|=v==0;for(auto&row:copy)zero|=row[c]==0;if(zero)matrix[r][c]=0;}','int[][]copy=Arrays.stream(matrix).map(int[]::clone).toArray(int[][]::new);for(int r=0;r<matrix.length;r++)for(int c=0;c<matrix[r].length;c++){boolean zero=false;for(int v:copy[r])zero|=v==0;for(int[]row:copy)zero|=row[c]==0;if(zero)matrix[r][c]=0;}')}
    if mode=='tree_codec':return {'Serialize':ret(select('Probe.Serialize(root)','Probe.serialize(root)','Probe.serialize(root)','Probe::serialize(root)','Probe.serialize(root)')),'Deserialize':ret(select('Probe.Deserialize(encoded)','Probe.deserialize(encoded)','Probe.deserialize(encoded)','Probe::deserialize(encoded)','Probe.deserialize(encoded)'))}
    if mode=='strings_codec':return {
      'Encode':select('return string.Concat(strings.Select(s=>s.Length+":"+s));','return strings.map(s=>s.length+":"+s).join("");','return "".join(str(len(s))+":"+s for s in strings)','std::string out;for(auto&s:strings)out+=std::to_string(s.size())+":"+s;return out;','StringBuilder out=new StringBuilder();for(String s:strings)out.append(s.length()).append(":").append(s);return out.toString();'),
      'Decode':select('var outp=new List<string>();int i=0;while(i<encoded.Length){int j=encoded.IndexOf(\':\',i),n=int.Parse(encoded[i..j]);i=j+1;outp.Add(encoded.Substring(i,n));i+=n;}return outp.ToArray();','const out=[];let i=0;while(i<encoded.length){const j=encoded.indexOf(":",i),n=Number(encoded.slice(i,j));i=j+1;out.push(encoded.slice(i,i+n));i+=n;}return out;','out=[];i=0\nwhile i<len(encoded):\n    j=encoded.index(":",i);n=int(encoded[i:j]);i=j+1;out.append(encoded[i:i+n]);i+=n\nreturn out','std::vector<std::string>out;size_t i=0;while(i<encoded.size()){auto j=encoded.find(\':\',i);auto n=std::stoul(encoded.substr(i,j-i));i=j+1;out.push_back(encoded.substr(i,n));i+=n;}return out;','List<String>out=new ArrayList<>();int i=0;while(i<encoded.length()){int j=encoded.indexOf(\':\',i),n=Integer.parseInt(encoded.substring(i,j));i=j+1;out.add(encoded.substring(i,i+n));i+=n;}return out.toArray(String[]::new);')}
    if mode in ('trie','dictionary'):
        insert='Insert' if mode=='trie' else 'AddWord'
        bodies={insert:select('words.Add(word);','this.words.add(word);','self.words.add(word)','words.insert(word);','words.add(word);')}
        if mode=='trie':bodies.update(Search=ret(select('words.Contains(word)','this.words.has(word)','word in self.words','words.count(word)!=0','words.contains(word)')),StartsWith=ret(select('words.Any(w=>w.StartsWith(prefix,StringComparison.Ordinal))','[...this.words].some(w=>w.startsWith(prefix))','any(w.startswith(prefix) for w in self.words)','std::any_of(words.begin(),words.end(),[&](const auto&w){return w.compare(0,prefix.size(),prefix)==0;})','words.stream().anyMatch(w->w.startsWith(prefix))')))
        else:bodies['Search']=select('return words.Any(w=>w.Length==pattern.Length&&w.Select((c,i)=>pattern[i]==\'.\'||pattern[i]==c).All(v=>v));','return [...this.words].some(w=>w.length===pattern.length&&[...w].every((c,i)=>pattern[i]==="."||pattern[i]===c));','return any(len(w)==len(pattern) and all(p=="." or p==c for p,c in zip(pattern,w)) for w in self.words)','for(auto&w:words){if(w.size()!=pattern.size())continue;bool ok=true;for(size_t i=0;i<w.size();i++)ok&=pattern[i]==\'.\'||pattern[i]==w[i];if(ok)return true;}return false;','for(String w:words){if(w.length()!=pattern.length())continue;boolean ok=true;for(int i=0;i<w.length();i++)ok&=pattern.charAt(i)==\'.\'||pattern.charAt(i)==w.charAt(i);if(ok)return true;}return false;')
        return bodies
    if mode=='median':return {'AddNum':select('values.Add(value);values.Sort();','this.values.push(value);this.values.sort((a,b)=>a-b);','self.values.append(value);self.values.sort()','values.push_back(value);std::sort(values.begin(),values.end());','values.add(value);Collections.sort(values);'),'FindMedian':select('int n=values.Count;return ((double)values[(n-1)/2]+values[n/2])/2;','const n=this.values.length;return (this.values[Math.floor((n-1)/2)]+this.values[Math.floor(n/2)])/2;','n=len(self.values)\nreturn (self.values[(n-1)//2]+self.values[n//2])/2','auto n=values.size();return (static_cast<double>(values[(n-1)/2])+values[n/2])/2;','int n=values.size();return ((double)values.get((n-1)/2)+values.get(n/2))/2;')}
    return None

def python_oracle(s):
    oracle=(ROOT/'scripts/blind75/oracle.py').read_text()
    oracle=oracle.replace('class Node:','class OracleNode:').replace('Node(', 'OracleNode(')
    arg=', '.join(p['name'] for p in s['params'])
    return {s['method']:f'return solve(SPEC, [{arg}])'},'\n'+oracle+'\nSPEC='+repr({k:s[k] for k in ['method','mode','title','id']})+'\n'

def fixture(s,lang,cases,variant="correct"):
    fields="";helper=None
    bodies=bodymap(s,lang) or ordinary_body(s,lang);extra=PROBES[lang] if bodies else ''
    if bodies is None:
        assert lang=='python', (s['id'],lang)
        bodies,extra=python_oracle(s)
    if variant=='incorrect':bodies,extra,fields,helper=negative_fixture(s,lang,bodies,extra)
    source=starter(s,lang,bodies)['starterCode']
    if helper:
        if lang in ('python','javascript'):source+='\n'+helper
        else:source=source.replace('class Solution {','class Solution {\n'+helper)
    if fields:
        cls=STATE[s['mode']][0]
        source=source.replace('class '+cls+(':' if lang=='python' else ' {'),'class '+cls+(':' if lang=='python' else ' {')+'\n'+fields)
    if lang=='cpp':source=source.replace('class '+STATE.get(s['mode'],('Solution',[]))[0]+' {',extra+'\nclass '+STATE.get(s['mode'],('Solution',[]))[0]+' {')
    else:source+='\n'+extra
    if s['mode'] in ('trie','dictionary','median'):
        cls=STATE[s['mode']][0];median=s['mode']=='median'
        fields={'csharp':'private '+('List<int> values=new();' if median else 'HashSet<string> words=new();'), 'java':'private '+('List<Integer> values=new ArrayList<>();' if median else 'Set<String> words=new HashSet<>();'),'cpp':('std::vector<int> values;' if median else 'std::set<std::string> words;'),'javascript':'constructor(){this.'+('values=[]' if median else 'words=new Set()')+';}','python':'    def __init__(self): self.'+('values=[]' if median else 'words=set()')+'\n'}[lang]
        source=source.replace('class '+cls+(':' if lang=='python' else ' {'),'class '+cls+(':' if lang=='python' else ' {')+'\n'+fields)
    return source

def generate():
    catalog=json.loads((ROOT/'blind75/catalog.json').read_text())
    for s in catalog:
        cases=json.loads((ROOT/'blind75/cases'/f'{s["id"]}.json').read_text())
        for lang in LANGS:
            for variant in ['correct','incorrect']:
                source=fixture(s,lang,cases,variant)
                path=ROOT/'scripts/blind75/fixtures'/variant/lang/s['id']/s['starters'][lang]['filename'];path.parent.mkdir(parents=True,exist_ok=True);path.write_text(source)
    print('Generated 375 actual algorithm fixtures and 375 nonconstant/contract-breaking negative fixtures.')
if __name__=='__main__':generate()
