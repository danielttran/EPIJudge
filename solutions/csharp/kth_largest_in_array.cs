public class Solution
{
    public int FindKthLargest(int k, List<int> A)
    {
        int target = k - 1, low = 0, high = A.Count - 1;
        while (low <= high)
        {
            int pivot = A[low + (high - low) / 2];
            int greater = low, scan = low, smaller = high;
            while (scan <= smaller)
            {
                if (A[scan] > pivot)
                {
                    (A[greater], A[scan]) = (A[scan], A[greater]);
                    greater++;
                    scan++;
                }
                else if (A[scan] < pivot)
                {
                    (A[scan], A[smaller]) = (A[smaller], A[scan]);
                    smaller--;
                }
                else
                    scan++;
            }
            if (target < greater)
                high = greater - 1;
            else if (target > smaller)
                low = smaller + 1;
            else
                return A[target];
        }
        throw new ArgumentOutOfRangeException(nameof(k));
    }
}
