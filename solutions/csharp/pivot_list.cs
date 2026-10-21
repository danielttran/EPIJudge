using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public ListNode<int>? ListPivoting(ListNode<int>? head, int x)
    {
        var less = new ListNode<int>(0);
        var equal = new ListNode<int>(0);
        var greater = new ListNode<int>(0);
        var lessTail = less;
        var equalTail = equal;
        var greaterTail = greater;
        while (head is not null)
        {
            var next = head.Next;
            head.Next = null;
            if (head.Data < x)
            {
                lessTail.Next = head;
                lessTail = head;
            }
            else if (head.Data == x)
            {
                equalTail.Next = head;
                equalTail = head;
            }
            else
            {
                greaterTail.Next = head;
                greaterTail = head;
            }
            head = next;
        }
        equalTail.Next = greater.Next;
        lessTail.Next = equal.Next;
        return less.Next;
    }
}
