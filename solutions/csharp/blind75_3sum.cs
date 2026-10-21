using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public int[][] ThreeSum(int[] nums)
    {
        Array.Sort(nums);
        var outp = new List<int[]>();
        for (int i = 0; i < nums.Length; i++)
        {
            if (i > 0 && nums[i] == nums[i - 1])
                continue;
            int l = i + 1, r = nums.Length - 1;
            while (l < r)
            {
                int sum = nums[i] + nums[l] + nums[r];
                if (sum < 0)
                    l++;
                else if (sum > 0)
                    r--;
                else
                {
                    outp.Add([nums[i], nums[l], nums[r]]);
                    int x = nums[l], y = nums[r];
                    while (l < r && nums[l] == x)
                        l++;
                    while (l < r && nums[r] == y)
                        r--;
                }
            }
        }
        return outp.ToArray();
    }
}

// Shared node types from the supplied starter.
public class ListNode
{
    public int val;
    public ListNode? next;
    public ListNode(int val = 0, ListNode? next = null)
    {
        this.val = val;
        this.next = next;
    }
}
public class TreeNode
{
    public int val;
    public TreeNode? left, right;
    public TreeNode(int val = 0, TreeNode? left = null, TreeNode? right = null)
    {
        this.val = val;
        this.left = left;
        this.right = right;
    }
}
public class Node
{
    public int val;
    public List<Node> neighbors = new();
    public Node(int val = 0)
    {
        this.val = val;
    }
}
