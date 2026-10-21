using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    private readonly Dictionary<string, long> credits = new();
    private readonly SortedSet<(long Credit, string Id)> ranking = new();
    private long offset;

    public void Initialize()
    {
        credits.Clear();
        ranking.Clear();
        offset = 0;
    }

    public void Insert(string clientId, int credit)
    {
        Remove(clientId);
        long normalized = credit - offset;
        credits[clientId] = normalized;
        ranking.Add((normalized, clientId));
    }

    public bool Remove(string clientId)
    {
        if (!credits.Remove(clientId, out long normalized))
            return false;
        ranking.Remove((normalized, clientId));
        return true;
    }

    public int Lookup(string clientId) =>
        credits.TryGetValue(clientId, out long normalized) ? (int)(normalized + offset) : -1;

    public void AddAll(int amount) => offset += amount;

    public string Max() => ranking.Count == 0 ? "" : ranking.Max.Id;
}
