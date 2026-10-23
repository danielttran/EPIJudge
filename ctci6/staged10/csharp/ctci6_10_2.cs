using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public List<string> GroupAnagrams(string[] words)
    {
        var decorated = new(string Key, string Word)[words.Length];
        for (int i = 0; i < words.Length; ++i)
        {
            var letters = words[i].ToCharArray();
            Array.Sort(letters);
            decorated[i] = (new string(letters), words[i]);
        }
        Array.Sort(decorated, (a, b) => StringComparer.Ordinal.Compare(a.Key, b.Key));
        for (int i = 0; i < words.Length; ++i)
            words[i] = decorated[i].Word;
        return new List<string>(words);
    }
}
