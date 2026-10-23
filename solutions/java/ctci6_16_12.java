import java.util.*;
class Solution {
  public List<String> EncodeXml(String[] elementNames, String[] elementTexts, int[][] children,
      int[] attributeOwners, String[] attributeNames, String[] attributeValues, String[] codeNames,
      int[] codes) {
    var result = new ArrayList<String>();
    if (elementNames.length == 0)
      return result;
    var lookup = new HashMap<String, String>();
    for (int i = 0; i < codeNames.length; ++i)
      lookup.put(codeNames[i], Integer.toString(codes[i]));
    var attributes = new ArrayList<ArrayList<Integer>>();
    for (int i = 0; i < elementNames.length; ++i)
      attributes.add(new ArrayList<>());
    for (int i = 0; i < attributeOwners.length; ++i)
      attributes.get(attributeOwners[i]).add(i);
    var events = new ArrayDeque<int[]>();
    events.push(new int[] {0, 0});
    while (!events.isEmpty()) {
      int[] frame = events.pop();
      int node = frame[0];
      if (frame[1] != 0) {
        result.add("0");
        continue;
      }
      result.add(lookup.get(elementNames[node]));
      for (int attribute : attributes.get(node)) {
        result.add(lookup.get(attributeNames[attribute]));
        result.add(attributeValues[attribute]);
      }
      result.add("0");
      events.push(new int[] {node, 1});
      if (!elementTexts[node].isEmpty())
        result.add(elementTexts[node]);
      else
        for (int i = children[node].length - 1; i >= 0; --i)
          events.push(new int[] {children[node][i], 0});
    }
    return result;
  }
}
