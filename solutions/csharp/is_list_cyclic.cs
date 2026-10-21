using EpiJudge.TestFramework;
public class Solution
{
    public ListNode<int>? HasCycle(ListNode<int>? head)
    {
        var slow = head;
        var fast = head;
        while (fast?.Next is not null)
        {
            slow = slow!.Next;
            fast = fast.Next.Next;
            if (!ReferenceEquals(slow, fast))
                continue;
            var entry = head;
            while (!ReferenceEquals(entry, slow))
            {
                entry = entry!.Next;
                slow = slow!.Next;
            }
            return entry;
        }
        return null;
    }
}
