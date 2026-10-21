public class Solution
{
    public List<int> IntersectTwoSortedArrays(List<int> A, List<int> B)
    {
        var result = new List<int>();
        int i = 0, j = 0;
        while (i < A.Count && j < B.Count)
        {
            if (A[i] < B[j])
                i++;
            else if (A[i] > B[j])
                j++;
            else
            {
                if (result.Count == 0 || result[^1] != A[i])
                    result.Add(A[i]);
                i++;
                j++;
            }
        }
        return result;
    }
}
