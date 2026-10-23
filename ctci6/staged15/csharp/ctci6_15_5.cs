using System;
using System.Collections.Generic;
using System.Text;
public abstract class SyncContext {public abstract void Wait(int gate);public abstract void Signal(int gate);public abstract void Work();}
public class Solution
{
    public void RunOrdered(int role, SyncContext context)
    {
        if (role > 0)
            context.Wait(role - 1);
        context.Work();
        if (role < 2)
            context.Signal(role);
    }
}
