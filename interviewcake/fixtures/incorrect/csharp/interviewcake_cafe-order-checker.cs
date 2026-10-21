using System;
using System.Collections.Generic;
using System.Linq;
using System.IO;
using System.Text;
// Bank-supplied data types and injected randomness. No problem logic is hidden here.
public class LinkedListNode { public int Value; public LinkedListNode? Next; public LinkedListNode(int value, LinkedListNode? next=null) { Value=value; Next=next; } }
public class BinaryTreeNode { public int Value; public BinaryTreeNode? Left, Right; public BinaryTreeNode(int value) { Value=value; } }
public class GraphNode { public string Label; public HashSet<GraphNode> Neighbors=new(); public string? Color; public GraphNode(string label) { Label=label; } }
public class Meeting { public int StartTime, EndTime; public Meeting(int start,int end) { StartTime=start; EndTime=end; } }
public class Rectangle { public int LeftX, BottomY, Width, Height; public Rectangle(int x=0,int y=0,int width=0,int height=0) { LeftX=x; BottomY=y; Width=width; Height=height; } }
public class CakeType { public int Weight; public long Value; public CakeType(int weight,long value) { Weight=weight; Value=value; } }
public record FilePaths(string OriginalPath,string DuplicatePath);
public class InfinityException : Exception { public InfinityException():base("Unbounded optimum") {} }
public static class RandomSource {
    public static Func<int,int,int> Draw = (lower,upper) => throw new InvalidOperationException("Random source must be injected by the judge.");
    public static int GetRandom(int lower,int upper) => Draw(lower,upper);
    public static int Rand5() => GetRandom(1,5);
    public static int Rand7() => GetRandom(1,7);
}
public class Solution
{
    public bool IsFirstComeFirstServed(int[] takeOut,int[] dineIn,int[] served)
    {
        var available=new HashSet<int>(takeOut.Concat(dineIn));
        return served.Length==takeOut.Length+dineIn.Length && served.All(available.Remove);
    }
}
