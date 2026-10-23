using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int MaximumBoxStackHeight(int[][] boxes)
    {
        int n = boxes.Length;
        int[] order = new int[n], heights = new int[n];
        for (int i = 0; i < n; ++i)
            order[i] = i;
        Array.Sort(order, (a, b) => boxes[a][0].CompareTo(boxes[b][0]));
        int best = 0;
        for (int i = 0; i < n; ++i)
        {
            int current = order[i];
            heights[i] = boxes[current][1];
            for (int j = 0; j < i; ++j)
            {
                int top = order[j];
                if (boxes[top][0] < boxes[current][0] && boxes[top][1] < boxes[current][1] &&
                    boxes[top][2] < boxes[current][2])
                    heights[i] = Math.Max(heights[i], boxes[current][1] + heights[j]);
            }
            best = Math.Max(best, heights[i]);
        }
        return best;
    }
}
