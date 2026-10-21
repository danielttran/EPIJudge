using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<List<int>> NQueens(int n)
    {
        var answer = new List<List<int>>();
        var placement = new List<int>();
        var columns = new HashSet<int>();
        var rising = new HashSet<int>();
        var falling = new HashSet<int>();
        void Place(int row)
        {
            if (row == n)
            {
                answer.Add(new List<int>(placement));
                return;
            }
            for (int c = 0; c < n; c++)
            if (!columns.Contains(c) && !rising.Contains(row + c) && !falling.Contains(row - c))
            {
                columns.Add(c);
                rising.Add(row + c);
                falling.Add(row - c);
                placement.Add(c);
                Place(row + 1);
                placement.RemoveAt(placement.Count - 1);
                columns.Remove(c);
                rising.Remove(row + c);
                falling.Remove(row - c);
            }
        }
        Place(0);
        return answer;
    }
}
