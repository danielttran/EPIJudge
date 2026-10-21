import java.util.*;
import java.io.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.util.function.IntBinaryOperator;
// Bank-supplied data types and injected randomness; no hidden algorithm helpers.
class LinkedListNode { public int Value; public LinkedListNode Next; LinkedListNode(int value){Value=value;} LinkedListNode(int value,LinkedListNode next){Value=value;Next=next;} }
class BinaryTreeNode { public int Value; public BinaryTreeNode Left,Right; BinaryTreeNode(int value){Value=value;} }
class GraphNode { public String Label,Color; public Set<GraphNode> Neighbors=new HashSet<>(); GraphNode(String label){Label=label;} }
class Meeting { public int StartTime,EndTime; Meeting(int start,int end){StartTime=start;EndTime=end;} }
class Rectangle { public int LeftX,BottomY,Width,Height; Rectangle(){this(0,0,0,0);} Rectangle(int x,int y,int width,int height){LeftX=x;BottomY=y;Width=width;Height=height;} }
class CakeType { public int Weight; public long Value; CakeType(int weight,long value){Weight=weight;Value=value;} }
class FilePaths { public String OriginalPath,DuplicatePath; FilePaths(String original,String duplicate){OriginalPath=original;DuplicatePath=duplicate;} }
class InfinityException extends RuntimeException { InfinityException(){super("Unbounded optimum");} }
class RandomSource { public static IntBinaryOperator Draw=(lower,upper)->{throw new IllegalStateException("Random source must be injected by judge");}; public static int GetRandom(int lower,int upper){return Draw.applyAsInt(lower,upper);} public static int Rand5(){return GetRandom(1,5);} public static int Rand7(){return GetRandom(1,7);} }
class TempTracker {
    private final int[] frequencies=new int[111];private int count,mode,minimum=111,maximum=-1;private long sum;
    public void Insert(int temperature){frequencies[temperature]++;count++;sum+=temperature;minimum=Math.min(minimum,temperature);maximum=Math.max(maximum,temperature);if(frequencies[temperature]>frequencies[mode])mode=temperature;}
    public Integer GetMin(){return count==0?null:minimum;}
    public Integer GetMax(){return count==0?null:maximum;}
    public Double GetMean(){return count==0?null:(double)sum/count;}
    public Integer GetMode(){return count==0?null:mode;}
}
