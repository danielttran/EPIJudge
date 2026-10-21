public class Solution
{
    public List<double> FindClosestKStars(List<(double, double, double)> stars, int k)
    {
        var selected = new PriorityQueue<double, double>();
        foreach (var (x, y, z) in stars)
        {
            double squared = x * x + y * y + z * z;
            selected.Enqueue(squared, -squared);
            if (selected.Count > k)
                selected.Dequeue();
        }
        var result = new List<double>();
        while (selected.TryDequeue(out double squared, out _))
            result.Add(Math.Sqrt(squared));
        return result;
    }
}
