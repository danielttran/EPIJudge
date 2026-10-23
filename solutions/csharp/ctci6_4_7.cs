using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int[] BuildOrder(int projectCount, int[][] dependencies)
    {
        var adjacent = new List<int>[projectCount];
        for (int i = 0; i < projectCount; ++i)
            adjacent[i] = new List<int>();
        int[] indegree = new int[projectCount];
        foreach (var edge in dependencies)
        {
            adjacent[edge[0]].Add(edge[1]);
            ++indegree[edge[1]];
        }
        var order = new List<int>();
        for (int i = 0; i < projectCount; ++i)
            if (indegree[i] == 0)
                order.Add(i);
        for (int head = 0; head < order.Count; ++head)
            foreach (int dependent in adjacent[order[head]])
            {
                --indegree[dependent];
                if (indegree[dependent] == 0)
                    order.Add(dependent);
            }
        return order.Count == projectCount ? order.ToArray() : [];
    }
}
