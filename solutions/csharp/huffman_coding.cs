public class Solution
{
    public double HuffmanEncoding(List<(string, double)> symbols)
    {
        var weights = new PriorityQueue<double, double>();
        foreach (var (_, frequency) in symbols)
            weights.Enqueue(frequency, frequency);
        double cost = 0;
        while (weights.Count > 1)
        {
            double combined = weights.Dequeue() + weights.Dequeue();
            cost += combined;
            weights.Enqueue(combined, combined);
        }
        return cost / 100.0;
    }
}
