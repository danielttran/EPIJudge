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
    private static String Fingerprint(Path file) throws IOException {
        long size=Files.size(file);int count=(int)Math.min(64L,size);
        long end=Math.max(0L,size-64L); long[] offsets={0L,end/2L,end};
        StringBuilder key=new StringBuilder().append(size);
        try(RandomAccessFile input=new RandomAccessFile(file.toFile(),"r")){
            for(long offset:offsets){byte[] sample=new byte[count];input.seek(offset);input.readFully(sample);key.append(':').append(Base64.getEncoder().encodeToString(sample));}
        }
        return key.toString();
    }
    public List<FilePaths> FindDuplicateFiles(String startingDirectory) {
        var firstByFingerprint=new HashMap<String,Path>();var result=new ArrayList<FilePaths>();
        try(var paths=Files.walk(Paths.get(startingDirectory))){
            var files=paths.filter(Files::isRegularFile).iterator();
            while(files.hasNext()){
                Path file=files.next().toAbsolutePath().normalize();String key=Long.toString(Files.size(file));
                Path earlier=firstByFingerprint.putIfAbsent(key,file);
                if(earlier!=null){
                    Path original=earlier,duplicate=file;
                    if(Files.getLastModifiedTime(file).toMillis()<Files.getLastModifiedTime(earlier).toMillis()){original=file;duplicate=earlier;}
                    result.add(new FilePaths(original.toString(),duplicate.toString()));
                }
            }
        }catch(IOException error){throw new UncheckedIOException(error);}
        return result;
    }
}
