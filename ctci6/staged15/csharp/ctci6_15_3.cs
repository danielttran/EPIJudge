using System;
using System.Collections.Generic;
using System.Text;
public abstract class ForkContext {public abstract void Take(int fork);public abstract void Drop(int fork);public abstract void Eat();}
public class Solution
{
    public void Dine(int role, int philosophers, int bites, ForkContext context)
    {
        int left = role, right = (role + 1) % philosophers, lower = Math.Min(left, right),
            higher = Math.Max(left, right);
        for (int bite = 0; bite < bites; ++bite)
        {
            context.Take(lower);
            context.Take(higher);
            context.Eat();
            context.Drop(higher);
            context.Drop(lower);
        }
    }
}
