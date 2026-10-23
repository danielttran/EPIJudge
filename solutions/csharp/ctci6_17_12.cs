using System;
using System.Collections.Generic;
using System.Text;
public class BiNode { public int Data; public BiNode? Node1; public BiNode? Node2; public BiNode(int data){Data=data;} }
public class Solution
{
    public BiNode? ConvertBiNode(BiNode? root)
    {
        var stack = new Stack<BiNode>();
        BiNode? current = root, previous = null, head = null;
        while (current is not null || stack.Count > 0)
        {
            while (current is not null)
            {
                stack.Push(current);
                current = current.Node1;
            }
            var node = stack.Pop();
            var right = node.Node2;
            node.Node1 = previous;
            if (previous is null)
                head = node;
            else
                previous.Node2 = node;
            previous = node;
            current = right;
        }
        if (previous is not null)
            previous.Node2 = null;
        return head;
    }
}
