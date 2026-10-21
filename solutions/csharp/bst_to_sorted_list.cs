using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public BinaryTreeNode<int>? BstToDoublyLinkedList(BinaryTreeNode<int>? tree)
    {
        var stack = new Stack<BinaryTreeNode<int>>();
        BinaryTreeNode<int>? head = null, previous = null, current = tree;
        while (current is not null || stack.Count > 0)
        {
            while (current is not null)
            {
                stack.Push(current);
                current = current.Left;
            }
            current = stack.Pop();
            var right = current.Right;
            current.Left = previous;
            if (previous is null)
                head = current;
            else
                previous.Right = current;
            previous = current;
            current = right;
        }
        if (previous is not null)
            previous.Right = null;
        return head;
    }
}
