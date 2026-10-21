using EpiJudge.TestFramework;
public class Solution
{
    public bool IsLinkedListAPalindrome(ListNode<int>? L)
    {
        if (L?.Next is null)
            return true;
        var middle = L;
        var fast = L;
        while (fast.Next?.Next is not null)
        {
            middle = middle.Next!;
            fast = fast.Next.Next;
        }
        ListNode<int>? Reverse(ListNode<int>? node)
        {
            ListNode<int>? previous = null;
            while (node is not null)
            {
                var next = node.Next;
                node.Next = previous;
                previous = node;
                node = next;
            }
            return previous;
        }
        var second = Reverse(middle.Next);
        bool equal = true;
        var left = L;
        for (var right = second; right is not null; right = right.Next)
        {
            if (left.Data != right.Data)
                equal = false;
            left = left.Next!;
        }
        middle.Next = Reverse(second);
        return equal;
    }
}
