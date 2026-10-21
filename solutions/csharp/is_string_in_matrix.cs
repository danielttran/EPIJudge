public class Solution
{
    public bool IsPatternContainedInGrid(List<List<int>> grid, List<int> pattern)
    {
        if (pattern.Count == 0)
            return true;
        if (grid.Count == 0 || grid[0].Count == 0)
            return false;
        int rows = grid.Count, columns = grid[0].Count;
        var reachable = new bool[rows, columns];
        for (int r = 0; r < rows; r++)
        for (int c = 0; c < columns; c++)
            reachable[r, c] = grid[r][c] == pattern[0];
        for (int i = 1; i < pattern.Count; i++)
        {
            var next = new bool[rows, columns];
            for (int r = 0; r < rows; r++)
            for (int c = 0; c < columns; c++)
                next[r, c] = grid[r][c] == pattern[i] &&
                    ((r > 0 && reachable[r - 1, c]) || (r + 1 < rows && reachable[r + 1, c]) ||
                     (c > 0 && reachable[r, c - 1]) || (c + 1 < columns && reachable[r, c + 1]));
            reachable = next;
        }
        foreach (bool found in reachable)
        if (found)
            return true;
        return false;
    }
}
