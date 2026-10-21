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
    private record Entry(BinaryTreeNode node, int depth) {}
    public boolean IsBalanced(BinaryTreeNode root) {
        if (root == null) return true;
        ArrayDeque<Entry> pending = new ArrayDeque<>(); pending.push(new Entry(root,0));
        int shallowest = Integer.MAX_VALUE, deepest = 0;
        while (!pending.isEmpty()) {
            Entry current = pending.pop(); BinaryTreeNode node = current.node();
            if (node.Left == null && node.Right == null) {
                shallowest = Math.min(shallowest,current.depth()); deepest = Math.max(deepest,current.depth());
                if (deepest-shallowest > 1) return false;
            }
            if (node.Left != null) pending.push(new Entry(node.Left,current.depth()+1));
            if (node.Right != null) pending.push(new Entry(node.Right,current.depth()+1));
        }
        return true;
    }
}
