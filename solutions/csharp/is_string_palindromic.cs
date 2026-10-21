public class Solution
{
    public bool IsPalindromic(string s)
    {
        for (int left = 0, right = s.Length - 1; left < right; left++, right--)
            if (s[left] != s[right])
                return false;
        return true;
    }
}
