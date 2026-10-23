import java.util.*;
abstract class BitArray { public abstract int Size(); public abstract int FetchBit(int index,int column); }
class Solution {
  public int MissingNumberBits(BitArray numbers) {
    var current = new ArrayList<Integer>();
    for (int i = 0; i < numbers.Size(); ++i)
      current.add(i);
    int answer = 0, column = 0;
    while (!current.isEmpty() && column < 32) {
      var zeros = new ArrayList<Integer>();
      var ones = new ArrayList<Integer>();
      for (int index : current)
        (numbers.FetchBit(index, column) == 0 ? zeros : ones).add(index);
      if (zeros.size() <= ones.size())
        current = zeros;
      else {
        answer |= 1 << column;
        current = ones;
      }
      column++;
    }
    return answer;
  }
}
