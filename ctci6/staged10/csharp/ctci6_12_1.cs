using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public List<string> LastKLines(string filePath, int k)
    {
        var suffix = new Queue<string>();
        foreach (string line in System.IO.File.ReadLines(filePath))
        {
            suffix.Enqueue(line);
            if (suffix.Count > k)
                suffix.Dequeue();
        }
        return new List<string>(suffix);
    }
}
