public class Solution
{
    public bool IsWellFormed(string s)
    {
        var openings = new Stack<char>();
        foreach (char c in s)
        {
            if (c is '(' or '[' or '{')
            {
                openings.Push(c);
                continue;
            }
            char expected = c switch
            {
                ')' => '(',
                ']' => '[',
                '}' => '{',
                _ => '\0'
            };
            if (expected == '\0' || !openings.TryPop(out char opening) || opening != expected)
                return false;
        }
        return openings.Count == 0;
    }
}
