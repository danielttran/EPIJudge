namespace EpiJudge.TestFramework;

public sealed class BinaryTreeNode<T>(T data)
{
    public T Data { get; set; } = data;
    public BinaryTreeNode<T>? Left { get; set; }
    public BinaryTreeNode<T>? Right { get; set; }
    public BinaryTreeNode<T>? Parent { get; set; }
}

public sealed class ListNode<T>(T data)
{
    public T Data { get; set; } = data;
    public ListNode<T>? Next { get; set; }
}
