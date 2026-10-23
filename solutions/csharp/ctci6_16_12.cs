using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public List<string> EncodeXml(string[] elementNames, string[] elementTexts, int[][] children,
                                  int[] attributeOwners, string[] attributeNames,
                                  string[] attributeValues, string[] codeNames, int[] codes)
    {
        var result = new List<string>();
        if (elementNames.Length == 0)
            return result;
        var lookup = new Dictionary<string, string>(StringComparer.Ordinal);
        for (int i = 0; i < codeNames.Length; ++i)
            lookup[codeNames[i]] =
                codes[i].ToString(System.Globalization.CultureInfo.InvariantCulture);
        var attributes = new List<int>[elementNames.Length];
        for (int i = 0; i < attributes.Length; ++i)
            attributes[i] = new List<int>();
        for (int i = 0; i < attributeOwners.Length; ++i)
            attributes[attributeOwners[i]].Add(i);
        var events = new Stack<(int Node, bool Exit)>();
        events.Push((0, false));
        while (events.Count > 0)
        {
            var frame = events.Pop();
            int node = frame.Node;
            if (frame.Exit)
            {
                result.Add("0");
                continue;
            }
            result.Add(lookup[elementNames[node]]);
            foreach (int attribute in attributes[node])
            {
                result.Add(lookup[attributeNames[attribute]]);
                result.Add(attributeValues[attribute]);
            }
            result.Add("0");
            events.Push((node, true));
            if (elementTexts[node].Length > 0)
                result.Add(elementTexts[node]);
            else
                for (int i = children[node].Length - 1; i >= 0; --i)
                    events.Push((children[node][i], false));
        }
        return result;
    }
}
