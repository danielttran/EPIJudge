public class Solution
{
    public bool IsValidSudoku(List<List<int>> partial_assignment)
    {
        int n = partial_assignment.Count;
        int width = (int)Math.Sqrt(n);
        if (n == 0)
            return true;
        if (width * width != n || partial_assignment.Any(row => row.Count != n))
            return false;
        var rows = Enumerable.Range(0, n).Select(_ => new HashSet<int>()).ToArray();
        var columns = Enumerable.Range(0, n).Select(_ => new HashSet<int>()).ToArray();
        var blocks = Enumerable.Range(0, n).Select(_ => new HashSet<int>()).ToArray();
        for (int r = 0; r < n; r++)
        for (int c = 0; c < n; c++)
        {
            int value = partial_assignment[r][c];
            if (value == 0)
                continue;
            if (value < 1 || value > n || !rows[r].Add(value) || !columns[c].Add(value) ||
                !blocks[(r / width) * width + c / width].Add(value))
                return false;
        }
        return true;
    }
}
