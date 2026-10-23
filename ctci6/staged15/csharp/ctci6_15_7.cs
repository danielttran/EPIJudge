using System;
using System.Collections.Generic;
using System.Text;
public abstract class FizzContext {public abstract void Wait(int gate);public abstract void Signal(int gate);public abstract void Print(int value);}
public class Solution
{
    public void RunFizzBuzz(int role, int limit, FizzContext context)
    {
        int Owner(int value) => value % 15 == 0 ? 3 : value % 3 == 0 ? 1 : value % 5 == 0 ? 2 : 0;
        for (int value = 1; value <= limit; ++value)
        {
            if (Owner(value) != role)
                continue;
            context.Wait(role);
            context.Print(value);
            if (value < limit)
                context.Signal(Owner(value + 1));
        }
    }
}
