public class Solution
{
    public List<string> DecomposeIntoDictionaryWords(string domain, HashSet<string> dictionary)
    {
        var previous = Enumerable.Repeat(-1, domain.Length + 1).ToArray();
        previous[0] = 0;
        for (int end = 1; end <= domain.Length; end++)
            for (int start = 0; start < end; start++)
                if (previous[start] != -1 && dictionary.Contains(domain[start..end]))
                {
                    previous[end] = start;
                    break;
                }
        if (previous[^1] == -1)
            return new List<string>();
        var words = new List<string>();
        for (int end = domain.Length; end > 0; end = previous[end])
            words.Add(domain[previous[end]..end]);
        words.Reverse();
        return words;
    }
}
