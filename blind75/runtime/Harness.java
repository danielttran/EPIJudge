import epi.test_framework.minimal_json.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.lang.reflect.*;
import java.util.*;

public class Harness {
  static class ContractError extends RuntimeException { ContractError(String text){super(text);} }
  static void check(boolean ok,String message){if(!ok)throw new ContractError(message);}
  static Object fresh(String name)throws Exception{return Class.forName(name).getDeclaredConstructor().newInstance();}
  static Object call(Object target,String name,Object...args)throws Exception{
    Method method=Arrays.stream(target.getClass().getMethods()).filter(m->m.getName().equals(name)).findFirst().orElseThrow();
    try{return method.invoke(target,args);}catch(InvocationTargetException ex){Throwable cause=ex.getCause();if(cause instanceof Exception e)throw e;throw ex;}
  }
  static List<ListNode> listNodes(ListNode head){
    List<ListNode> out=new ArrayList<>();Set<Object> seen=Collections.newSetFromMap(new IdentityHashMap<>());
    while(head!=null){check(seen.add(head),"Output list contains a cycle.");out.add(head);head=head.next;}return out;
  }
  static List<Object> nodes(Object root,String kind){
    List<Object> out=new ArrayList<>();
    if(kind.equals("list")){out.addAll(listNodes((ListNode)root));return out;}
    if(kind.equals("lists")){for(ListNode head:(ListNode[])root)out.addAll(listNodes(head));return out;}
    if(!kind.equals("tree")&&!kind.equals("graph"))return out;
    Set<Object> seen=Collections.newSetFromMap(new IdentityHashMap<>());Deque<Object> q=new ArrayDeque<>();if(root!=null)q.push(root);
    while(!q.isEmpty()){
      Object node=q.pop();if(!seen.add(node)){check(kind.equals("graph"),"Tree contains a cycle or shared child.");continue;}out.add(node);
      if(node instanceof Node n){q.addAll(n.neighbors);}else if(node instanceof TreeNode n){if(n.left!=null)q.push(n.left);if(n.right!=null)q.push(n.right);}
    }return out;
  }
  static int val(Object node){if(node instanceof ListNode n)return n.val;if(node instanceof TreeNode n)return n.val;return ((Node)node).val;}
  static List<Object> links(Object node){if(node instanceof ListNode n)return Arrays.asList(n.next);if(node instanceof TreeNode n)return Arrays.asList(n.left,n.right);return new ArrayList<>(((Node)node).neighbors);}
  static Object load(JsonValue v,String kind){
    if(kind.equals("list")){ListNode head=null;JsonArray a=v.asArray();for(int i=a.size()-1;i>=0;i--)head=new ListNode(a.get(i).asInt(),head);return head;}
    if(kind.equals("lists")){JsonArray a=v.asArray();ListNode[] out=new ListNode[a.size()];for(int i=0;i<out.length;i++)out[i]=(ListNode)load(a.get(i),"list");return out;}
    if(kind.equals("tree")){
      JsonArray a=v.asArray();if(a.size()==0)return null;TreeNode root=new TreeNode(a.get(0).asInt());Deque<TreeNode> q=new ArrayDeque<>();q.add(root);int i=1;
      while(!q.isEmpty()){
        TreeNode n=q.remove();if(i<a.size()&&!a.get(i).isNull()){n.left=new TreeNode(a.get(i).asInt());q.add(n.left);}i++;
        if(i<a.size()&&!a.get(i).isNull()){n.right=new TreeNode(a.get(i).asInt());q.add(n.right);}i++;
      }return root;
    }
    if(kind.equals("graph")){
      JsonArray a=v.asArray();Node[] nn=new Node[a.size()];for(int i=0;i<nn.length;i++)nn[i]=new Node(i+1);
      for(int i=0;i<nn.length;i++)for(JsonValue c:a.get(i).asArray())nn[i].neighbors.add(nn[c.asInt()-1]);return nn.length==0?null:nn[0];
    }
    switch(kind){
      case "i":return v.asInt();case "l":return v.asLong();case "s":return v.asString();case "b":return v.asBoolean();
      case "ai":{JsonArray a=v.asArray();int[] out=new int[a.size()];for(int i=0;i<out.length;i++)out[i]=a.get(i).asInt();return out;}
      case "as":{JsonArray a=v.asArray();String[] out=new String[a.size()];for(int i=0;i<out.length;i++)out[i]=a.get(i).asString();return out;}
      case "aai":{JsonArray a=v.asArray();int[][] out=new int[a.size()][];for(int i=0;i<out.length;i++)out[i]=(int[])load(a.get(i),"ai");return out;}
      case "aas":{JsonArray a=v.asArray();String[][] out=new String[a.size()][];for(int i=0;i<out.length;i++)out[i]=(String[])load(a.get(i),"as");return out;}
      case "ab":{JsonArray a=v.asArray();boolean[] out=new boolean[a.size()];for(int i=0;i<out.length;i++)out[i]=a.get(i).asBoolean();return out;}
      case "ad":{JsonArray a=v.asArray();double[] out=new double[a.size()];for(int i=0;i<out.length;i++)out[i]=a.get(i).asDouble();return out;}
      default:throw new IllegalArgumentException(kind);
    }
  }
  static JsonValue dump(Object value,String kind){
    if(kind.equals("list")){JsonArray out=new JsonArray();for(ListNode n:listNodes((ListNode)value))out.add(n.val);return out;}
    if(kind.equals("tree_node"))return value==null?Json.NULL:Json.value(((TreeNode)value).val);
    if(kind.equals("tree")){
      nodes(value,"tree");List<TreeNode> q=new ArrayList<>();List<JsonValue> values=new ArrayList<>();if(value!=null)q.add((TreeNode)value);
      for(int i=0;i<q.size();i++){TreeNode n=q.get(i);values.add(n==null?Json.NULL:Json.value(n.val));if(n!=null){q.add(n.left);q.add(n.right);}}
      while(!values.isEmpty()&&values.get(values.size()-1).isNull())values.remove(values.size()-1);JsonArray out=new JsonArray();for(JsonValue v:values)out.add(v);return out;
    }
    if(kind.equals("graph")){
      List<Object> nn=nodes(value,"graph");nn.sort(Comparator.comparingInt(Harness::val));JsonArray out=new JsonArray();
      for(int i=0;i<nn.size();i++){Node n=(Node)nn.get(i);check(n.val==i+1,"Graph labels must remain unique and contiguous.");int[] labels=n.neighbors.stream().mapToInt(c->c.val).sorted().toArray();out.add(dump(labels,"ai"));}return out;
    }
    if(value==null)return Json.NULL;
    if(value instanceof Boolean b)return Json.value(b);if(value instanceof String s)return Json.value(s);
    if(value instanceof Integer n)return Json.value(n);if(value instanceof Long n)return Json.value(n);if(value instanceof Double n)return Json.value(n);
    JsonArray out=new JsonArray();if(value instanceof Collection<?> c){for(Object v:c)out.add(dump(v,""));return out;}
    if(value.getClass().isArray()){for(int i=0;i<Array.getLength(value);i++)out.add(dump(Array.get(value,i),""));return out;}
    throw new IllegalArgumentException("Unsupported result type "+value.getClass());
  }
  static JsonValue execute(JsonArray raw)throws Exception{
    Object[] args=new Object[KINDS.length];for(int i=0;i<args.length;i++)args[i]=load(raw.get(i),KINDS[i]);
    List<Object> original=new ArrayList<>();for(int i=0;i<args.length;i++)original.addAll(nodes(args[i],KINDS[i]));
    IdentityHashMap<Object,Integer> snapshot=new IdentityHashMap<>();for(Object n:original)snapshot.put(n,val(n));
    IdentityHashMap<Object,List<Object>> originalLinks=new IdentityHashMap<>();for(Object n:original)originalLinks.put(n,links(n));
    int[][] rows=MODE.equals("matrix_inplace")?((int[][])args[0]).clone():new int[0][];
    String before=MODE.equals("tree_codec")||MODE.equals("graph_clone")?dump(args[0],KINDS[0]).toString():null;Object actual;
    switch(MODE){
      case "list_cycle":{
        List<ListNode> nn=listNodes((ListNode)args[0]);int pos=raw.get(1).asInt();if(pos>=0)nn.get(nn.size()-1).next=nn.get(pos);
        List<ListNode> edges=new ArrayList<>();for(ListNode n:nn)edges.add(n.next);actual=call(fresh("Solution"),METHOD,args);
        for(int i=0;i<nn.size();i++){check(nn.get(i).next==edges.get(i),"Cycle detection must preserve links.");check(nn.get(i).val==snapshot.get(nn.get(i)),"Cycle detection must preserve values.");}break;
      }
      case "strings_codec":actual=call(fresh("Codec"),"decode",call(fresh("Codec"),"encode",args[0]));break;
      case "tree_codec":actual=call(fresh("Codec"),"deserialize",call(fresh("Codec"),"serialize",args[0]));break;
      case "trie":case "dictionary":case "median":{
        Object obj=fresh(CLASS);List<Object> results=new ArrayList<>();String[] ops=(String[])args[0];
        for(int i=0;i<ops.length;i++){String op=ops[i];Object result=op.equals("findMedian")?call(obj,op):call(obj,op,Array.get(args[1],i));if(!Set.of("insert","addWord","addNum").contains(op))results.add(result);}actual=results;break;
      }
      default:actual=call(fresh("Solution"),METHOD,args);if(MODE.equals("matrix_inplace")||MODE.equals("list_reorder"))actual=args[0];
    }
    if(MODE.equals("matrix_inplace")){int[][] matrix=(int[][])args[0];check(rows.length==matrix.length,"Preserve rows.");for(int i=0;i<rows.length;i++)check(rows[i]==matrix[i],"Preserve each row object.");}
    if(Set.of("list_reuse","list_remove","list_reorder","tree_inplace","tree_node","tree_codec","graph_clone").contains(MODE)){
      String kind=MODE.startsWith("list_")?"list":MODE.equals("graph_clone")?"graph":"tree";
      List<Object> after=MODE.equals("tree_node")?(actual==null?List.of():List.of(actual)):nodes(actual,kind);
      Set<Object> expected=Collections.newSetFromMap(new IdentityHashMap<>());expected.addAll(original);
      if(MODE.equals("list_remove"))expected.remove(original.get(original.size()-(Integer)args[1]));
      if(Set.of("list_reuse","list_remove","list_reorder","tree_inplace").contains(MODE))check(expected.size()==after.size()&&expected.containsAll(after),"Reuse exactly the requested original nodes.");
      else if(MODE.equals("tree_node"))check(snapshot.containsKey(actual),"Return an original tree node.");
      else{for(Object n:after)check(!snapshot.containsKey(n),"Copy shares original nodes.");check(dump(args[0],KINDS[0]).toString().equals(before),"Preserve original structure.");for(Object n:original){List<Object>now=links(n),old=originalLinks.get(n);check(now.size()==old.size(),"Preserve original links.");if(kind.equals("graph")){for(Object previous:old)check(now.stream().anyMatch(v->v==previous),"Preserve original links.");}else for(int i=0;i<now.size();i++)check(now.get(i)==old.get(i),"Preserve original links.");}}
      for(Object n:original)check(val(n)==snapshot.get(n),"Preserve original node values.");if(MODE.equals("tree_inplace"))check(actual==args[0],"Return the original root.");
    }return dump(actual,OUTPUT);
  }
  public static void main(String[] ignored)throws Exception{
    JsonArray results=new JsonArray();JsonArray cases=Json.parse(Files.readString(Path.of("cases.json"),StandardCharsets.UTF_8)).asArray();
    for(JsonValue c:cases){long start=System.nanoTime();JsonValue actual=Json.NULL,error=Json.NULL;boolean invalid=false;
      java.io.PrintStream stdout=System.out;
      try{System.setOut(new java.io.PrintStream(java.io.OutputStream.nullOutputStream()));actual=execute(c.asArray());}catch(ContractError ex){invalid=true;}catch(Throwable ex){error=Json.value(ex.toString());}finally{System.setOut(stdout);}
      results.add(new JsonObject().add("actual",actual).add("error",error).add("validationFailed",invalid).add("elapsedMs",(System.nanoTime()-start)/1000000.0));
    }Files.writeString(Path.of("results.json"),results.toString(),StandardCharsets.UTF_8);
  }
// CONFIGURATION
}
