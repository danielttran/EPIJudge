using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    private sealed record Shape(Shape? Left, Shape? Right);

    public List<List<int>> GenerateAllBinaryTrees(int num_nodes)
    {
        var memo = new Dictionary<int, List<Shape?>>();
        List<Shape?> Generate(int count)
        {
            if (memo.TryGetValue(count, out var cached))
                return cached;
            var shapes = new List<Shape?>();
            if (count == 0)
                shapes.Add(null);
            else
                for (int left = 0; left < count; left++)
                    foreach (var first in Generate(left))
                        foreach (var second in Generate(count - 1 - left))
                            shapes.Add(new Shape(first, second));
            memo[count] = shapes;
            return shapes;
        }
        var result = new List<List<int>>();
        foreach (var shape in Generate(num_nodes))
        {
            var encoding = new List<int>();
            var queue = new Queue<Shape?>();
            queue.Enqueue(shape);
            while (queue.TryDequeue(out var node))
            {
                encoding.Add(node is null ? 0 : 1);
                if (node is not null)
                {
                    queue.Enqueue(node.Left);
                    queue.Enqueue(node.Right);
                }
            }
            result.Add(encoding);
        }
        return result;
    }
}
