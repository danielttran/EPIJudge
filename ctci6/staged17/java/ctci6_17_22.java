import java.util.*;
class Solution {
  public List<String> WordTransformation(String start, String stop, String[] dictionary) {
    Set<String> words = new HashSet<>(Arrays.asList(dictionary));
    Map<String, String> previous = new HashMap<>();
    previous.put(start, null);
    List<String> queue = new ArrayList<>();
    queue.add(start);
    for (int head = 0; head < queue.size(); ++head) {
      String word = queue.get(head);
      if (word.equals(stop)) {
        List<String> path = new ArrayList<>();
        for (String current = stop; current != null; current = previous.get(current))
          path.add(current);
        Collections.reverse(path);
        return path;
      }
      char[] letters = word.toCharArray();
      for (int position = 0; position < letters.length; ++position) {
        char original = letters[position];
        for (char letter = 'a'; letter <= 'z'; ++letter) {
          if (letter == original)
            continue;
          letters[position] = letter;
          String candidate = new String(letters);
          if (words.contains(candidate) && !previous.containsKey(candidate)) {
            previous.put(candidate, word);
            queue.add(candidate);
          }
        }
        letters[position] = original;
      }
    }
    return new ArrayList<>();
  }
}
