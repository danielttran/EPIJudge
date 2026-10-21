public class Solution
{
    public List<int> KLargestInBinaryHeap(List<int> A, int k)
    {
        var result = new List<int>();
        if (A.Count == 0 || k == 0)
            return result;
        var candidates = new PriorityQueue<int, long>();
        candidates.Enqueue(0, -(long)A[0]);
        while (result.Count < k && candidates.TryDequeue(out int index, out _))
        {
            result.Add(A[index]);
            int left = 2 * index + 1, right = left + 1;
            if (left < A.Count)
                candidates.Enqueue(left, -(long)A[left]);
            if (right < A.Count)
                candidates.Enqueue(right, -(long)A[right]);
        }
        return result;
    }
}
