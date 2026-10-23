import java.util.*;
class RandomNode { public int Data; public RandomNode Left,Right; public RandomNode(int data){Data=data;} }
class RandomSource { static java.util.function.IntBinaryOperator Draw=(lower,upper)->{throw new IllegalStateException("Provided by the judge");}; public static int GetRandom(int lower,int upper){return Draw.applyAsInt(lower,upper);} }
class RandomBst {
  private static final class SizedNode extends RandomNode {
    int Size = 1;
    SizedNode(int value) {
      super(value);
    }
  }
  public RandomNode Root;
  private static int size(RandomNode node) {
    return node == null ? 0 : ((SizedNode) node).Size;
  }
  public void Insert(int value) {
    var added = new SizedNode(value);
    if (Root == null) {
      Root = added;
      return;
    }
    var path = new ArrayList<RandomNode>();
    RandomNode node = Root;
    while (true) {
      path.add(node);
      if (value <= node.Data) {
        if (node.Left == null) {
          node.Left = added;
          break;
        }
        node = node.Left;
      } else {
        if (node.Right == null) {
          node.Right = added;
          break;
        }
        node = node.Right;
      }
    }
    for (var ancestor : path)
      ((SizedNode) ancestor).Size++;
  }
  public RandomNode Find(int value) {
    RandomNode node = Root;
    while (node != null) {
      if (value == node.Data)
        return node;
      node = value < node.Data ? node.Left : node.Right;
    }
    return null;
  }
  public boolean Delete(int value) {
    var path = new ArrayList<RandomNode>();
    RandomNode node = Root;
    while (node != null && node.Data != value) {
      path.add(node);
      node = value < node.Data ? node.Left : node.Right;
    }
    if (node == null)
      return false;
    if (node.Left != null && node.Right != null) {
      path.add(node);
      RandomNode successor = node.Right;
      while (successor.Left != null) {
        path.add(successor);
        successor = successor.Left;
      }
      node.Data = successor.Data;
      node = successor;
    }
    RandomNode replacement = node.Left != null ? node.Left : node.Right;
    if (path.isEmpty())
      Root = replacement;
    else {
      RandomNode parent = path.get(path.size() - 1);
      if (parent.Left == node)
        parent.Left = replacement;
      else
        parent.Right = replacement;
    }
    for (var ancestor : path)
      ((SizedNode) ancestor).Size--;
    return true;
  }
  public RandomNode GetRandomNode() {
    if (Root == null)
      return null;
    int rank = RandomSource.GetRandom(0, size(Root) - 1);
    RandomNode node = Root;
    while (node != null) {
      int leftSize = size(node.Left);
      if (rank < leftSize)
        node = node.Left;
      else if (rank == leftSize)
        return node;
      else {
        rank -= leftSize + 1;
        node = node.Right;
      }
    }
    return null;
  }
}
