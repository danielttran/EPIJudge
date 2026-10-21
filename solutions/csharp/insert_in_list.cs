using EpiJudge.TestFramework;
public class Solution
{
    public ListNode<int>? InsertList(ListNode<int>? l, int node_idx, int new_node_data)
    {
        var selected = l;
        for (int position = 1; position < node_idx; position++)
            selected = selected!.Next;
        if (selected is null)
            throw new ArgumentOutOfRangeException(nameof(node_idx));
        selected.Next = new ListNode<int>(new_node_data) { Next = selected.Next };
        return l;
    }
}
