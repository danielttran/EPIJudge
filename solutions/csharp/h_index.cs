public class Solution
{
    public int HIndex(List<int> citations)
    {
        int n = citations.Count;
        var counts = new int[n + 1];
        foreach (int citation in citations)
            counts[Math.Min(n, citation)]++;
        int papers = 0;
        for (int h = n; h >= 0; h--)
        {
            papers += counts[h];
            if (papers >= h)
                return h;
        }
        return 0;
    }
}
