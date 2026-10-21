using EpiJudge.TestFramework;
public class Solution
{
    public List<int> FindKLargestInBst(BinaryTreeNode<int>? tree, int k)
    {
        var result = new List<int>();
        var pending = new Stack<BinaryTreeNode<int>>();
        var current = tree;
        while (result.Count < k && (current is not null || pending.Count > 0))
        {
            while (current is not null)
            {
                pending.Push(current);
                current = current.Right;
            }
            current = pending.Pop();
            result.Add(current.Data);
            current = current.Left;
        }
        return result;
    }
}
