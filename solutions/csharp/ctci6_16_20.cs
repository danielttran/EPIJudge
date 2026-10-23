using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public List<string> T9Words(string digits, string[] dictionary)
    {
        const string mapping = "22233344455566677778889999";
        var result = new List<string>();
        foreach (string word in dictionary)
        {
            if (word.Length != digits.Length)
                continue;
            bool valid = true;
            for (int i = 0; i < word.Length; ++i)
                if (mapping[word[i] - 'a'] != digits[i])
                {
                    valid = false;
                    break;
                }
            if (valid)
                result.Add(word);
        }
        return result;
    }
}
