public class Solution
{
    public int FindKthInTwoSortedArrays(List<int> A, List<int> B, int k)
    {
        int a = 0, b = 0;
        while (true)
        {
            if (a == A.Count)
                return B[b + k - 1];
            if (b == B.Count)
                return A[a + k - 1];
            if (k == 1)
                return Math.Min(A[a], B[b]);
            int takeA = Math.Min(k / 2, A.Count - a);
            int takeB = Math.Min(k / 2, B.Count - b);
            if (A[a + takeA - 1] <= B[b + takeB - 1])
            {
                a += takeA;
                k -= takeA;
            }
            else
            {
                b += takeB;
                k -= takeB;
            }
        }
    }
}
