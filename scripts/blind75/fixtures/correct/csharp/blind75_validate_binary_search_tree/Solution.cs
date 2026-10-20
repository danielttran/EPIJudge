using System;
using System.Collections.Generic;
using System.Linq;
public class ListNode { public int val; public ListNode? next; public ListNode(int val=0,ListNode? next=null){this.val=val;this.next=next;} }
public class TreeNode { public int val; public TreeNode? left,right; public TreeNode(int val=0,TreeNode? left=null,TreeNode? right=null){this.val=val;this.left=left;this.right=right;} }
public class Node { public int val; public List<Node> neighbors=new(); public Node(int val=0){this.val=val;} }
public class Solution {
public bool IsValidBST(TreeNode? root) {
var a=Probe.Inorder(root).ToArray();return a.Zip(a.Skip(1)).All(p=>p.First<p.Second);
}
}


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
