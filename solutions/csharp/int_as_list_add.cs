using EpiJudge.TestFramework;
public class Solution
{
    public ListNode<int>? AddTwoNumbers(ListNode<int>? L1, ListNode<int>? L2)
    {
        var dummy = new ListNode<int>(0);
        var tail = dummy;
        int carry = 0;
        while (L1 is not null || L2 is not null || carry != 0)
        {
            int sum = (L1?.Data ?? 0) + (L2?.Data ?? 0) + carry;
            tail.Next = new ListNode<int>(sum % 10);
            tail = tail.Next;
            carry = sum / 10;
            L1 = L1?.Next;
            L2 = L2?.Next;
        }
        return dummy.Next;
    }
}
