public class Solution
{
    public int FindKthLargestUnknownLength(List<int> stream, int k)
    {
        var largest = new PriorityQueue<int, int>();
        foreach (int value in stream)
        {
            largest.Enqueue(value, value);
            if (largest.Count > k)
                largest.Dequeue();
        }
        return largest.Peek();
    }
}
