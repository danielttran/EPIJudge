import java.util.*;
class Solution {
  public List<String> LastKLines(String filePath, int k) {
    var suffix = new ArrayDeque<String>();
    try (var reader = new java.io.BufferedReader(new java.io.InputStreamReader(
             new java.io.FileInputStream(filePath), java.nio.charset.StandardCharsets.US_ASCII))) {
      String line;
      while ((line = reader.readLine()) != null) {
        suffix.addLast(line);
        if (suffix.size() > k)
          suffix.removeFirst();
      }
    } catch (java.io.IOException error) {
      throw new java.io.UncheckedIOException(error);
    }
    return new ArrayList<>(suffix);
  }
}
