import java.util.*;
abstract class LineRecord {public abstract int CompareTo(LineRecord other);public abstract void Release();}
abstract class TextFile {public abstract LineRecord ReadLine();public abstract void Rewind();public abstract void AppendLine(LineRecord record);public abstract void Close();}
abstract class TextWorkspace {public abstract TextFile CreateFile();public abstract void DeleteFile(TextFile file);}
class Solution {
  public TextFile SortExternalFile(TextFile inputFile, int bufferLimit, TextWorkspace workspace) {
    inputFile.Rewind();
    var runs = new ArrayList<TextFile>();
    while (true) {
      var chunk = new ArrayList<LineRecord>();
      for (int i = 0; i < bufferLimit; ++i) {
        var record = inputFile.ReadLine();
        if (record == null)
          break;
        chunk.add(record);
      }
      if (chunk.isEmpty())
        break;
      chunk.sort((first, second) -> first.CompareTo(second));
      var run = workspace.CreateFile();
      for (var record : chunk)
        run.AppendLine(record);
      run.Close();
      runs.add(run);
    }
    inputFile.Close();
    if (runs.isEmpty()) {
      var empty = workspace.CreateFile();
      empty.Close();
      return empty;
    }
    while (runs.size() > 1) {
      var merged = new ArrayList<TextFile>();
      for (int index = 0; index < runs.size(); index += 2) {
        if (index + 1 == runs.size()) {
          merged.add(runs.get(index));
          continue;
        }
        var left = runs.get(index);
        var right = runs.get(index + 1);
        left.Rewind();
        right.Rewind();
        var output = workspace.CreateFile();
        LineRecord first = left.ReadLine(), second = right.ReadLine();
        while (first != null || second != null) {
          if (second == null || (first != null && first.CompareTo(second) <= 0)) {
            output.AppendLine(first);
            first = left.ReadLine();
          } else {
            output.AppendLine(second);
            second = right.ReadLine();
          }
        }
        output.Close();
        left.Close();
        right.Close();
        workspace.DeleteFile(left);
        workspace.DeleteFile(right);
        merged.add(output);
      }
      runs = merged;
    }
    runs.get(0).Rewind();
    return runs.get(0);
  }
}
