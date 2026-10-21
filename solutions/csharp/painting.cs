using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<List<int>> FlipColor(int x, int y, List<List<int>> image)
    {
        if (image.Count == 0 || image[0].Count == 0)
            return image;
        int old = image[x][y], replacement = 1 - old;
        var queue = new Queue<(int Row, int Column)>();
        image[x][y] = replacement;
        queue.Enqueue((x, y));
        void Add(int r, int c)
        {
            if (r >= 0 && r < image.Count && c >= 0 && c < image[r].Count && image[r][c] == old)
            {
                image[r][c] = replacement;
                queue.Enqueue((r, c));
            }
        }
        while (queue.TryDequeue(out var cell))
        {
            Add(cell.Row - 1, cell.Column);
            Add(cell.Row + 1, cell.Column);
            Add(cell.Row, cell.Column - 1);
            Add(cell.Row, cell.Column + 1);
        }
        return image;
    }
}
