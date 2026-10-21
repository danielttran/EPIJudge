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
class Solution {
    public int HighestProductOf3(int[] values) {
        int highest=Math.max(values[0],values[1]),lowest=Math.min(values[0],values[1]);
        int highPair=values[0]*values[1],lowPair=highPair,best=highPair*values[2];
        for(int i=2;i<values.length;i++){
            int value=values[i];best=Math.max(best,Math.max(value*highPair,value*lowPair));
            highPair=Math.max(highPair,Math.max(value*highest,value*lowest));lowPair=Math.min(lowPair,Math.min(value*highest,value*lowest));
            highest=Math.max(highest,value);lowest=Math.min(lowest,value);
        }
        return best;
    }
}
