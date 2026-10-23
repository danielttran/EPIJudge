import java.util.*;
class Solution {
  public int[] ScoreMasterMind(String guess, String secret) {
    int[] remaining = new int[4];
    int hits = 0, pseudoHits = 0;
    for (int i = 0; i < 4; ++i) {
      if (guess.charAt(i) == secret.charAt(i))
        ++hits;
      else
        ++remaining["RGBY".indexOf(secret.charAt(i))];
    }
    for (int i = 0; i < 4; ++i) {
      if (guess.charAt(i) == secret.charAt(i))
        continue;
      int color = "RGBY".indexOf(guess.charAt(i));
      if (remaining[color] > 0) {
        --remaining[color];
        ++pseudoHits;
      }
    }
    return new int[] {hits, pseudoHits};
  }
}
