using System;
using System.Collections.Generic;
using System.Text;
public class RandomNode { public int Data; public RandomNode? Left,Right; public RandomNode(int data){Data=data;} }
public static class RandomSource { internal static Func<int,int,int> Draw=(lower,upper)=>throw new InvalidOperationException("Provided by the judge"); public static int GetRandom(int lower,int upper)=>Draw(lower,upper); }
public class RandomBst
{
    private sealed class SizedNode(int value) : RandomNode
    (value)
    {
        public int Size = 1;
    }
    public RandomNode? Root { get; private set; }
    private static int Size(RandomNode? node) => node is null ? 0 : ((SizedNode)node).Size;
    public void Insert(int value)
    {
        var added = new SizedNode(value);
        if (Root is null)
        {
            Root = added;
            return;
        }
        var path = new List<RandomNode>();
        var node = Root;
        while (true)
        {
            path.Add(node);
            if (value <= node.Data)
            {
                if (node.Left is null)
                {
                    node.Left = added;
                    break;
                }
                node = node.Left;
            }
            else
            {
                if (node.Right is null)
                {
                    node.Right = added;
                    break;
                }
                node = node.Right;
            }
        }
        foreach (var ancestor in path)
            ((SizedNode)ancestor).Size++;
    }
    public RandomNode? Find(int value)
    {
        var node = Root;
        while (node is not null)
        {
            if (value == node.Data)
                return node;
            node = value < node.Data ? node.Left : node.Right;
        }
        return null;
    }
    public bool Delete(int value)
    {
        var path = new List<RandomNode>();
        var node = Root;
        while (node is not null && node.Data != value)
        {
            path.Add(node);
            node = value < node.Data ? node.Left : node.Right;
        }
        if (node is null)
            return false;
        if (node.Left is not null && node.Right is not null)
        {
            path.Add(node);
            var successor = node.Right;
            while (successor.Left is not null)
            {
                path.Add(successor);
                successor = successor.Left;
            }
            node.Data = successor.Data;
            node = successor;
        }
        var replacement = node.Left ?? node.Right;
        if (path.Count == 0)
            Root = replacement;
        else
        {
            var parent = path[^1];
            if (ReferenceEquals(parent.Left, node))
                parent.Left = replacement;
            else
                parent.Right = replacement;
        }
        foreach (var ancestor in path)
            ((SizedNode)ancestor).Size--;
        return true;
    }
    public RandomNode? GetRandomNode()
    {
        if (Root is null)
            return null;
        int rank = RandomSource.GetRandom(0, Size(Root) - 1);
        var node = Root;
        while (node is not null)
        {
            int leftSize = Size(node.Left);
            if (rank < leftSize)
                node = node.Left;
            else if (rank == leftSize)
                return node;
            else
            {
                rank -= leftSize + 1;
                node = node.Right;
            }
        }
        return null;
    }
}
