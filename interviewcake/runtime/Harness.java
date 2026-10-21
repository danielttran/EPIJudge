import epi.test_framework.minimal_json.*;
import java.lang.reflect.Array;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

public class Harness {
    static final class ContractError extends RuntimeException {
        ContractError(String message) { super(message); }
    }
    static final class NeedChoice extends RuntimeException {
        final int lower, upper;
        NeedChoice(int lower, int upper) { this.lower=lower; this.upper=upper; }
    }
    // CONFIGURATION
    static void check(boolean condition, String message) {
        if (!condition) throw new ContractError(message);
    }
    static Exception cause(InvocationTargetException exception) {
        Throwable underlying=exception.getCause();
        if (underlying instanceof Exception error) return error;
        if (underlying instanceof Error error) throw error;
        return exception;
    }
    static Object fresh() throws Exception {
        try { return Class.forName(ClassName).getDeclaredConstructor().newInstance(); }
        catch (InvocationTargetException exception) { throw cause(exception); }
    }
    static Object call(Object instance, String name, Object... arguments) throws Exception {
        Method method=Arrays.stream(instance.getClass().getMethods())
            .filter(candidate -> candidate.getName().equals(name) && candidate.getParameterCount()==arguments.length)
            .findFirst().orElseThrow();
        try { return method.invoke(instance,arguments); }
        catch (InvocationTargetException exception) { throw cause(exception); }
    }
    static <T> Set<T> identities() { return Collections.newSetFromMap(new IdentityHashMap<>()); }
    static List<LinkedListNode> listNodes(LinkedListNode head) {
        var result=new ArrayList<LinkedListNode>(); Set<LinkedListNode> seen=identities();
        while (head!=null) {
            check(seen.add(head),"Output list contains a cycle.");
            result.add(head); head=head.Next;
        }
        return result;
    }
    static List<BinaryTreeNode> treeNodes(BinaryTreeNode root) {
        var result=new ArrayList<BinaryTreeNode>(); Set<BinaryTreeNode> seen=identities();
        var pending=new ArrayDeque<BinaryTreeNode>(); if(root!=null) pending.push(root);
        while (!pending.isEmpty()) {
            var node=pending.pop(); check(seen.add(node),"Input must remain a tree."); result.add(node);
            if(node.Left!=null) pending.push(node.Left); if(node.Right!=null) pending.push(node.Right);
        }
        return result;
    }
    static Object load(JsonValue value,String kind) {
        switch(kind) {
            case "tree": {
                if(value.isNull())return null;
                JsonArray array=value.asArray(); if(array.size()==0)return null;
                var root=new BinaryTreeNode(array.get(0).asInt());var queue=new ArrayDeque<BinaryTreeNode>();queue.add(root);int index=1;
                while(!queue.isEmpty()) {
                    var node=queue.remove();
                    if(index<array.size()&&!array.get(index).isNull()){node.Left=new BinaryTreeNode(array.get(index).asInt());queue.add(node.Left);}index++;
                    if(index<array.size()&&!array.get(index).isNull()){node.Right=new BinaryTreeNode(array.get(index).asInt());queue.add(node.Right);}index++;
                }
                return root;
            }
            case "list": {
                JsonArray array=value.asArray();LinkedListNode head=null;
                for(int index=array.size()-1;index>=0;index--)head=new LinkedListNode(array.get(index).asInt(),head);
                return head;
            }
            case "graph": {
                JsonArray array=value.asArray();GraphNode[] nodes=new GraphNode[array.size()];
                for(int index=0;index<nodes.length;index++)nodes[index]=new GraphNode("v"+index);
                for(int index=0;index<nodes.length;index++)for(JsonValue neighbor:array.get(index).asArray())nodes[index].Neighbors.add(nodes[neighbor.asInt()]);
                return nodes;
            }
            case "meetings": {
                var result=new ArrayList<Meeting>();
                for(JsonValue interval:value.asArray()){JsonArray pair=interval.asArray();result.add(new Meeting(pair.get(0).asInt(),pair.get(1).asInt()));}
                return result;
            }
            case "rect": {
                JsonArray rectangle=value.asArray();return new Rectangle(rectangle.get(0).asInt(),rectangle.get(1).asInt(),rectangle.get(2).asInt(),rectangle.get(3).asInt());
            }
            case "cakes": {
                JsonArray array=value.asArray();CakeType[] result=new CakeType[array.size()];
                for(int index=0;index<result.length;index++){JsonArray pair=array.get(index).asArray();result[index]=new CakeType(pair.get(0).asInt(),pair.get(1).asLong());}
                return result;
            }
            case "chars": return value.asString().toCharArray();
            case "i": return value.asInt();
            case "l": return value.asLong();
            case "s": case "files": return value.asString();
            case "ai": {
                JsonArray array=value.asArray();int[] result=new int[array.size()];for(int index=0;index<result.length;index++)result[index]=array.get(index).asInt();return result;
            }
            case "as": {
                JsonArray array=value.asArray();String[] result=new String[array.size()];for(int index=0;index<result.length;index++)result[index]=array.get(index).asString();return result;
            }
            case "map": {
                var result=new LinkedHashMap<String,String[]>();
                for(Member member:value.asObject())result.put(member.getName(),(String[])load(member.getValue(),"as"));return result;
            }
            default: throw new IllegalArgumentException("Unknown parameter kind "+kind);
        }
    }
    static JsonValue dump(Object value,String kind) {
        if(kind.equals("list")) {
            JsonArray result=new JsonArray();for(var node:listNodes((LinkedListNode)value))result.add(node.Value);return result;
        }
        if(value==null)return Json.NULL;
        switch(kind) {
            case "tree": {
                JsonArray result=new JsonArray();
                for(var node:treeNodes((BinaryTreeNode)value))result.add(new JsonArray().add(node.Value).add(node.Left==null?Json.NULL:Json.value(node.Left.Value)).add(node.Right==null?Json.NULL:Json.value(node.Right.Value)));
                return result;
            }
            case "meetings": {
                JsonArray result=new JsonArray();for(Object entry:(Collection<?>)value){Meeting meeting=(Meeting)entry;result.add(new JsonArray().add(meeting.StartTime).add(meeting.EndTime));}return result;
            }
            case "rect": {
                Rectangle rectangle=(Rectangle)value;return new JsonArray().add(rectangle.LeftX).add(rectangle.BottomY).add(rectangle.Width).add(rectangle.Height);
            }
            case "cakes": {
                JsonArray result=new JsonArray();for(CakeType cake:(CakeType[])value)result.add(new JsonArray().add(cake.Weight).add(cake.Value));return result;
            }
            case "chars": return Json.value(new String((char[])value));
            case "pairs": {
                JsonArray result=new JsonArray();for(Object entry:(Collection<?>)value){FilePaths paths=(FilePaths)entry;result.add(new JsonArray().add(paths.OriginalPath).add(paths.DuplicatePath));}return result;
            }
            default: break;
        }
        if(value instanceof JsonValue json)return json;
        if(value instanceof String string)return Json.value(string);
        if(value instanceof Character character)return Json.value(character.toString());
        if(value instanceof Boolean bool)return Json.value(bool);
        if(value instanceof Float || value instanceof Double)return Json.value(((Number)value).doubleValue());
        if(value instanceof Number number)return Json.value(number.longValue());
        if(value instanceof Map<?,?> map) {
            var ordered=new TreeMap<String,Object>();for(var entry:map.entrySet())ordered.put((String)entry.getKey(),entry.getValue());
            JsonObject result=new JsonObject();for(var entry:ordered.entrySet())result.add(entry.getKey(),dump(entry.getValue(),""));return result;
        }
        if(value instanceof Collection<?> collection){JsonArray result=new JsonArray();for(Object entry:collection)result.add(dump(entry,""));return result;}
        if(value.getClass().isArray()){JsonArray result=new JsonArray();for(int index=0;index<Array.getLength(value);index++)result.add(dump(Array.get(value,index),""));return result;}
        throw new IllegalArgumentException("Unsupported result type "+value.getClass().getName());
    }
    record TreeState(BinaryTreeNode node,int value,BinaryTreeNode left,BinaryTreeNode right) {}
    record ListState(LinkedListNode node,int value,LinkedListNode next) {}
    static Runnable preserve(Object[] arguments) {
        var trees=new ArrayList<TreeState>();var lists=new ArrayList<ListState>();var checks=new ArrayList<Runnable>();
        String[] before=new String[arguments.length];
        for(int index=0;index<arguments.length;index++) {
            Object argument=arguments[index];String kind=Kinds[index];before[index]=dump(argument,kind).toString();
            if(argument instanceof BinaryTreeNode root)for(var node:treeNodes(root))trees.add(new TreeState(node,node.Value,node.Left,node.Right));
            if(argument instanceof LinkedListNode head)for(var node:listNodes(head))lists.add(new ListState(node,node.Value,node.Next));
            if(kind.equals("meetings")) {
                List<?> meetings=(List<?>)argument;Object[] references=meetings.toArray();
                checks.add(()->{check(meetings.size()==references.length,"Meeting list size changed.");for(int position=0;position<references.length;position++)check(meetings.get(position)==references[position],"Meeting objects and list order must be preserved.");});
            }
            if(kind.equals("cakes")) {
                CakeType[] cakes=(CakeType[])argument;CakeType[] references=cakes.clone();
                checks.add(()->{for(int position=0;position<cakes.length;position++)check(cakes[position]==references[position],"Cake objects must be preserved.");});
            }
            if(kind.equals("map")) {
                Map<?,?> map=(Map<?,?>)argument;var references=new HashMap<Object,Object>();references.putAll(map);
                checks.add(()->{check(map.size()==references.size(),"Network keys changed.");for(var entry:references.entrySet())check(map.get(entry.getKey())==entry.getValue(),"Network neighbor-array objects must be preserved.");});
            }
        }
        return ()->{
            for(TreeState saved:trees)check(saved.node().Value==saved.value()&&saved.node().Left==saved.left()&&saved.node().Right==saved.right(),"Tree values and links must remain unchanged.");
            for(ListState saved:lists)check(saved.node().Value==saved.value()&&saved.node().Next==saved.next(),"List values and links must remain unchanged.");
            for(Runnable identityCheck:checks)identityCheck.run();
            for(int index=0;index<arguments.length;index++)check(dump(arguments[index],Kinds[index]).toString().equals(before[index]),"Read-only input was modified.");
        };
    }
    static String filesSnapshot(String rootName) throws Exception {
        Path root=Path.of(rootName);var entries=new ArrayList<String>();
        try(var paths=Files.walk(root)) {
            for(Path path:paths.filter(path->!path.equals(root)).sorted().toList()) {
                String relative=root.relativize(path).toString();
                if(Files.isDirectory(path))entries.add("D:"+relative);
                else entries.add("F:"+relative+":"+Files.getLastModifiedTime(path)+":"+HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(path))));
            }
        }
        return String.join("\n",entries);
    }
    static JsonValue state(JsonArray raw) throws Exception {
        Object instance=fresh();JsonArray operations=raw.get(0).asArray(),values=raw.get(1).asArray();JsonArray result=new JsonArray();int count=0;
        for(int index=0;index<operations.size();index++) {
            String method=operations.get(index).asString();JsonArray encoded=values.get(index).asArray();Object[] arguments=new Object[encoded.size()];
            for(int argument=0;argument<arguments.length;argument++)arguments[argument]=encoded.get(argument).isString()?encoded.get(argument).asString():encoded.get(argument).asInt();
            boolean empty=count==0&&((Mode.equals("queue")&&method.equals("Dequeue"))||(Mode.equals("stack")&&(method.equals("Pop")||method.equals("GetMax"))));
            try {Object actual=call(instance,method,arguments);check(!empty,"Empty-state operation must signal an error.");result.add(dump(actual,""));}
            catch(Exception error) {if(empty&&!(error instanceof ContractError)&&!(error instanceof NeedChoice))result.add(new JsonObject().add("error","empty"));else throw error;}
            if(method.equals("Enqueue")||method.equals("Push"))count++;
            else if((method.equals("Dequeue")||method.equals("Pop"))&&!empty)count--;
        }
        return result;
    }
    static boolean sameMultiset(int[] first,int[] second) {
        int[] a=first.clone(),b=second.clone();Arrays.sort(a);Arrays.sort(b);return Arrays.equals(a,b);
    }
    record Decision(int[] prefix,double weight) {}
    static void bounds(boolean shuffle,int length,int maximum,int lower,int upper) {
        check(lower<=upper&&(shuffle?lower>=0&&upper<Math.max(1,length):lower==1&&upper==maximum),"Unexpected random-source bounds.");
    }
    static int randomOutcome(Object result,int draws,int outcomes) {
        check(draws>0,"Use the supplied random source.");
        if(Mode.equals("rand7"))check(draws%2==0,"Rand7 requires two Rand5 draws per completed attempt.");
        check(result instanceof Integer && (Integer)result>=1&&(Integer)result<=outcomes,"Die result is outside its range.");
        return (Integer)result;
    }
    static long nextSeed(long seed) {return (seed*1664525L+1013904223L)&0xffffffffL;}
    static Object randomCheck(JsonArray raw) throws Exception {
        boolean shuffle=Mode.equals("shuffle");int maximum=Mode.equals("rand5")?7:5,outcomes=Mode.equals("rand5")?5:7;
        int[] original=shuffle?(int[])load(raw.get(0),"ai"):new int[0];
        int[] forced=shuffle?new int[0]:(int[])load(raw.get(0),"ai");
        var probabilities=new HashMap<String,Double>();double unresolved=0;int branches=0;
        var pending=new ArrayDeque<Decision>();pending.push(new Decision(new int[0],1));
        while(!pending.isEmpty()) {
            var decision=pending.pop();check(++branches<=100000,"Randomized algorithm used too many decision branches.");int[] position={0},draws={0};
            RandomSource.Draw=(lower,upper)->{
                check(++draws[0]<=128,"Randomized algorithm exceeded the draw budget.");bounds(shuffle,original.length,maximum,lower,upper);
                if(position[0]>=decision.prefix().length)throw new NeedChoice(lower,upper);
                int chosen=decision.prefix()[position[0]++];check(chosen>=lower&&chosen<=upper,"Invalid injected random choice.");return chosen;
            };
            int[] values=original.clone();
            try {
                Object actual=shuffle?call(fresh(),Method,(Object)values):call(fresh(),Method);String key;
                if(shuffle){check(sameMultiset(values,original),"Shuffle changed element multiplicities.");key=Arrays.toString(values);}
                else key=Integer.toString(randomOutcome(actual,draws[0],outcomes));
                probabilities.put(key,probabilities.getOrDefault(key,0.0)+decision.weight());
            } catch(NeedChoice next) {
                int limit=shuffle?Math.max(8,original.length*2):8;
                if(decision.prefix().length>=limit){unresolved+=decision.weight();continue;}
                for(int choice=next.lower;choice<=next.upper;choice++) {
                    int[] prefix=Arrays.copyOf(decision.prefix(),decision.prefix().length+1);prefix[prefix.length-1]=choice;
                    pending.push(new Decision(prefix,decision.weight()/(next.upper-next.lower+1)));
                }
            }
        }
        if(shuffle) {
            if(Arrays.stream(original).distinct().count()==original.length&&original.length<=5) {
                int factorial=1;for(int value=2;value<=original.length;value++)factorial*=value;
                check(unresolved<1e-10&&probabilities.size()==factorial,"Shuffle does not produce every permutation.");
                for(double probability:probabilities.values())check(Math.abs(probability-1.0/factorial)<1e-9,"Shuffle is biased over full permutations.");
            }
        } else {
            check(unresolved<0.02,"Rejection probability exceeds bounded judge exploration.");
            for(int outcome=1;outcome<=outcomes;outcome++) {
                double probability=probabilities.getOrDefault(Integer.toString(outcome),0.0);
                check(probability<=1.0/outcomes+1e-9&&probability+unresolved>=1.0/outcomes-1e-9,"Die transformation is biased over injected choices.");
            }
        }
        long[] seed={0x85ebca6bL};int[] counts=new int[outcomes+1];int samples=4096;
        boolean trackPermutations=shuffle&&original.length<=5&&Arrays.stream(original).distinct().count()==original.length;
        var sampledPermutations=new HashMap<String,Integer>();
        int[] pairs=new int[outcomes*outcomes],triples=new int[outcomes*outcomes*outcomes];
        int previous=-1,previousPrevious=-1;Object seededInstance=fresh();
        for(int trial=0;trial<samples;trial++) {
            int[] draws={0};final boolean useForced=trial==0&&!shuffle;
            RandomSource.Draw=(lower,upper)->{
                check(++draws[0]<=128,"Too many random draws.");bounds(shuffle,original.length,maximum,lower,upper);
                if(useForced&&draws[0]<=forced.length){int chosen=forced[draws[0]-1];check(chosen>=lower&&chosen<=upper,"Forced source choice is outside its bounds.");return chosen;}
                seed[0]=nextSeed(seed[0]);return lower+(int)((seed[0]*(upper-lower+1L))>>>32);
            };
            int[] values=original.clone();Object actual=shuffle?call(seededInstance,Method,(Object)values):call(seededInstance,Method);
            if(shuffle){
                check(sameMultiset(values,original),"Shuffle changed elements.");
                if(values.length>1)check(draws[0]>0,"Use the supplied random source.");
                if(trackPermutations){String permutation=Arrays.toString(values);sampledPermutations.merge(permutation,1,Integer::sum);}
            }
            else {
                int outcome=randomOutcome(actual,draws[0],outcomes)-1;counts[outcome+1]++;
                if(previous>=0)pairs[previous*outcomes+outcome]++;
                if(previousPrevious>=0)triples[(previousPrevious*outcomes+previous)*outcomes+outcome]++;
                previousPrevious=previous;previous=outcome;
            }
        }
        if(trackPermutations){
            int factorial=1;for(int value=2;value<=original.length;value++)factorial*=value;
            check(sampledPermutations.size()==factorial,"Repeated shuffles must produce every permutation.");
            double expected=(double)samples/factorial,chiSquared=0;
            for(int count:sampledPermutations.values())chiSquared+=(count-expected)*(count-expected)/expected;
            check(chiSquared<=4*(factorial-1)+80,"Repeated shuffles are biased over full permutations.");
        }
        if(!shuffle){
            double expected=(double)samples/outcomes,chiSquared=0;
            for(int outcome=1;outcome<=outcomes;outcome++)chiSquared+=(counts[outcome]-expected)*(counts[outcome]-expected)/expected;
            check(chiSquared<40,"Seeded die distribution is biased.");
            double pairExpected=(double)(samples-1)/pairs.length,pairChiSquared=0;
            for(int count:pairs)pairChiSquared+=(count-pairExpected)*(count-pairExpected)/pairExpected;
            check(pairChiSquared<4*(pairs.length-1)+80,"Consecutive die outcomes are dependent.");
            double tripleExpected=(double)(samples-2)/triples.length,tripleChiSquared=0;
            for(int count:triples)tripleChiSquared+=(count-tripleExpected)*(count-tripleExpected)/tripleExpected;
            check(tripleChiSquared<4*(triples.length-1)+80,"Three consecutive die outcomes are dependent.");
        }
        return true;
    }
    static Object execute(JsonArray raw) throws Exception {
        if(Set.of("queue","stack","trie","temperature").contains(Mode))return state(raw);
        if(Mode.equals("wordcloud")) {
            Object instance;
            try {instance=Class.forName(ClassName).getDeclaredConstructor(String.class).newInstance(raw.get(0).asString());}
            catch(InvocationTargetException exception){throw cause(exception);}
            return instance.getClass().getField("WordsToCounts").get(instance);
        }
        if(Set.of("shuffle","rand5","rand7").contains(Mode))return randomCheck(raw);
        if(Mode.equals("cycle")) {
            var head=(LinkedListNode)load(raw.get(0),"list");var nodes=listNodes(head);int cycle=raw.get(1).asInt();
            if(cycle>=0)nodes.get(nodes.size()-1).Next=nodes.get(cycle);
            var snapshots=new ArrayList<ListState>();for(var node:nodes)snapshots.add(new ListState(node,node.Value,node.Next));
            Object actual=call(fresh(),Method,head);
            for(var before:snapshots)check(before.node().Value==before.value()&&before.node().Next==before.next(),"Cycle detection modified the list.");
            return actual;
        }
        if(Mode.equals("delete")) {
            var head=(LinkedListNode)load(raw.get(0),"list");var nodes=listNodes(head);int target=raw.get(1).asInt();
            var snapshots=new ArrayList<ListState>();for(var node:nodes)snapshots.add(new ListState(node,node.Value,node.Next));
            call(fresh(),Method,nodes.get(target));
            for(int index=0;index<nodes.size();index++) {
                var expected=snapshots.get(index==target?target+1:index);var node=nodes.get(index);
                check(node.Value==expected.value()&&node.Next==expected.next(),"Deletion violated target/successor alias semantics.");
            }
            return dump(head,"list");
        }
        if(Mode.equals("reverse_list")) {
            var head=(LinkedListNode)load(raw.get(0),"list");var before=listNodes(head);int[] values=before.stream().mapToInt(node->node.Value).toArray();
            Object actual=call(fresh(),Method,head);var after=listNodes((LinkedListNode)actual);
            check(before.size()==after.size(),"Reversal must retain every original node.");
            for(int index=0;index<before.size();index++)check(after.get(index)==before.get(before.size()-1-index)&&before.get(index).Value==values[index],"Reversal must reuse original nodes in reverse order with unchanged values.");
            return dump(actual,"list");
        }
        Object[] arguments=new Object[Kinds.length];for(int index=0;index<Kinds.length;index++)arguments[index]=load(raw.get(index),Kinds[index]);
        if(Mode.equals("chars")||Mode.equals("words")) {
            char[] characters=(char[])arguments[0];call(fresh(),Method,arguments);
            check(characters.length==raw.get(0).asString().length(),"Array length changed.");return new String(characters);
        }
        if(Mode.equals("color")) {
            GraphNode[] nodes=(GraphNode[])arguments[0];GraphNode[] originalNodes=nodes.clone();String[] labels=new String[nodes.length];
            var originalSets=new ArrayList<Set<GraphNode>>();var edges=new ArrayList<Set<GraphNode>>();
            for(int index=0;index<nodes.length;index++){labels[index]=nodes[index].Label;originalSets.add(nodes[index].Neighbors);edges.add(new HashSet<>(nodes[index].Neighbors));}
            String[] colors=(String[])arguments[1],palette=colors.clone();call(fresh(),Method,arguments);
            for(int index=0;index<nodes.length;index++) {
                GraphNode node=nodes[index];check(node==originalNodes[index],"Preserve graph node identities.");
                check(Objects.equals(node.Label,labels[index])&&node.Neighbors==originalSets.get(index)&&node.Neighbors.equals(edges.get(index)),"Graph labels, neighbor sets and edges must be preserved.");
                check(node.Color!=null&&Arrays.asList(palette).contains(node.Color),"Every node needs a palette color.");
                for(GraphNode neighbor:node.Neighbors)check(!Objects.equals(node.Color,neighbor.Color),"Adjacent nodes have the same color.");
            }
            check(Arrays.equals(colors,palette),"Palette was modified.");return true;
        }
        Runnable preserve=preserve(arguments);String filesBefore=Mode.equals("files")?filesSnapshot((String)arguments[0]):null;Object actual;
        try{actual=call(fresh(),Method,arguments);}
        catch(InfinityException unbounded){preserve.run();return new JsonObject().add("error","infinite");}
        preserve.run();
        if(Mode.equals("files")){check(filesSnapshot((String)arguments[0]).equals(filesBefore),"Filesystem must remain unchanged.");return dump(actual,"pairs");}
        if(Mode.equals("kth")) {
            var nodes=listNodes((LinkedListNode)arguments[1]);int index=-1;for(int position=0;position<nodes.size();position++)if(nodes.get(position)==actual){index=position;break;}
            check(index>=0,"Return an original node reference.");return index;
        }
        if(Mode.equals("meetings")) {
            check(actual instanceof List<?> && actual!=arguments[0],"Return a new interval list.");
            Set<Object> originals=identities();originals.addAll((List<?>)arguments[0]);
            for(Object interval:(List<?>)actual)check(interval instanceof Meeting&&!originals.contains(interval),"Return new interval objects.");
        }
        if(Mode.equals("rect"))check(actual instanceof Rectangle&&actual!=arguments[0]&&actual!=arguments[1],"Return a new rectangle.");
        if(Result.equals("ai")){check(actual instanceof int[],"Return an int array.");for(Object argument:arguments)check(actual!=argument,"Return a newly allocated result array.");}
        return dump(actual,Result);
    }
    public static void main(String[] ignored) throws Exception {
        JsonArray rows=Json.parse(Files.readString(Path.of("cases.json"))).asArray(),output=new JsonArray();
        for(JsonValue encoded:rows) {
            long start=System.nanoTime();Object actual=null;String error=null;boolean validation=false;
            try{actual=execute(encoded.asArray());}
            catch(ContractError failure){validation=true;error=failure.getMessage();}
            catch(Throwable failure){error=failure.getClass().getSimpleName()+": "+failure.getMessage();}
            JsonObject row=new JsonObject().add("Actual",dump(actual,"")).add("Error",error==null?Json.NULL:Json.value(error))
                .add("ElapsedMs",(System.nanoTime()-start)/1000000.0).add("ValidationFailed",validation);
            output.add(row);
        }
        Files.writeString(Path.of("results.json"),output.toString());
    }
}
