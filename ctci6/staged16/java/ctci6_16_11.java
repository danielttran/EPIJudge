import java.util.*;
class Solution {
  public int[] DivingBoardLengths(int planks, int shorter, int longer) {
    if (shorter == longer)
      return new int[] {planks * shorter};
    int[] result = new int[planks + 1];
    for (int count = 0; count <= planks; ++count)
      result[count] = planks * shorter + count * (longer - shorter);
    return result;
  }
}
