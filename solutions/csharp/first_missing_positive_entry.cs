public class Solution
{
    public int FindFirstMissingPositive(List<int> A)
    {
        for (int i = 0; i < A.Count; i++)
            while (A[i] >= 1 && A[i] <= A.Count && A[A[i] - 1] != A[i])
            {
                int destination = A[i] - 1;
                (A[i], A[destination]) = (A[destination], A[i]);
            }
        for (int i = 0; i < A.Count; i++)
        if (A[i] != i + 1)
            return i + 1;
        return A.Count + 1;
    }
}
