using EpiJudge.TestFramework;
public class Solution
{
    public GraphVertex CloneGraph(GraphVertex graph)
    {
        var copies = new Dictionary<GraphVertex, GraphVertex>();
        var pending = new Queue<GraphVertex>();
        copies.Add(graph, new GraphVertex(graph.Label));
        pending.Enqueue(graph);
        while (pending.TryDequeue(out var original))
            foreach (var neighbor in original.Edges)
            {
                if (!copies.TryGetValue(neighbor, out var copy))
                {
                    copy = new GraphVertex(neighbor.Label);
                    copies.Add(neighbor, copy);
                    pending.Enqueue(neighbor);
                }
                copies[original].Edges.Add(copy);
            }
        return copies[graph];
    }
}
