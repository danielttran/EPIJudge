public class Solution
{
    public bool IsLetterConstructibleFromMagazine(string letter_text, string magazine_text)
    {
        var needed = new Dictionary<char, int>();
        foreach (char c in letter_text)
            needed[c] = needed.GetValueOrDefault(c) + 1;
        int remaining = letter_text.Length;
        foreach (char c in magazine_text)
            if (needed.TryGetValue(c, out int count) && count > 0)
            {
                needed[c] = count - 1;
                remaining--;
            }
        return remaining == 0;
    }
}
