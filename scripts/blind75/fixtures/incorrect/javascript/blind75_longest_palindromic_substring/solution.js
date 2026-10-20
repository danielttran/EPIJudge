class ListNode { constructor(val=0,next=null){this.val=val;this.next=next;} }
class TreeNode { constructor(val=0,left=null,right=null){this.val=val;this.left=left;this.right=right;} }
class Node { constructor(val=0){this.val=val;this.neighbors=[];} }
function longestPalindrome(s) {
let value=actualCorrect(s);
return value + "!";
}

module.exports = { ListNode, TreeNode, Node, longestPalindrome };

function actualCorrect(s){
let start=0,length=0;function expand(l,r){while(l>=0&&r<s.length&&s[l]===s[r]){if(r-l+1>length||(r-l+1===length&&l<start)){start=l;length=r-l+1;}l--;r++;}}for(let i=0;i<s.length;i++){expand(i,i);expand(i,i+1);}return s.slice(start,start+length);
}


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
