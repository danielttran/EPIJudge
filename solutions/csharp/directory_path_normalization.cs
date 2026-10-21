using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public string ShortestEquivalentPath(string path)
    {
        bool absolute = path.StartsWith('/');
        var components = new List<string>();
        foreach (string part in path.Split('/', StringSplitOptions.RemoveEmptyEntries))
        {
            if (part == ".")
                continue;
            if (part == "..")
            {
                if (components.Count > 0 && components[^1] != "..")
                    components.RemoveAt(components.Count - 1);
                else if (!absolute)
                    components.Add("..");
            }
            else
                components.Add(part);
        }
        return (absolute ? "/" : "") + string.Join('/', components);
    }
}
