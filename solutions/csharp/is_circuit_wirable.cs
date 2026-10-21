public class Solution
{
    public bool IsAnyPlacementFeasible(int k, List<(int, int)> edges)
    {
        var neighbors = Enumerable.Range(0, k).Select(_ => new List<int>()).ToArray();
        foreach (var (a, b) in edges)
        {
            neighbors[a].Add(b);
            neighbors[b].Add(a);
        }
        var colors = Enumerable.Repeat(-1, k).ToArray();
        var queue = new Queue<int>();
        for (int start = 0; start < k; start++)
        {
            if (colors[start] != -1)
                continue;
            colors[start] = 0;
            queue.Enqueue(start);
            while (queue.TryDequeue(out int node))
                foreach (int next in neighbors[node])
                {
                    if (colors[next] == colors[node])
                        return false;
                    if (colors[next] != -1)
                        continue;
                    colors[next] = 1 - colors[node];
                    queue.Enqueue(next);
                }
        }
        return true;
    }
}
