using System;
using System.Collections.Generic;
using System.Text;
public class LinkedListNode { public int Value; public LinkedListNode? Next; public LinkedListNode(int value, LinkedListNode? next = null) { Value = value; Next = next; } }
public class Solution
{
    public bool IsPalindrome(LinkedListNode? head)
    {
        var values = new List<int>();
        for (LinkedListNode? p = head; p != null; p = p.Next)
            values.Add(p.Value);
        int n = values.Count;
        for (int i = 0; i < n / 2; ++i)
            if (values[i] != values[n - 1 - i])
                return false;
        return true;
    }
}
