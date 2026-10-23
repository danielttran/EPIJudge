using System;
using System.Collections.Generic;
using System.Text;
public abstract class LineRecord {public abstract int CompareTo(LineRecord other);public abstract void Release();}
public abstract class TextFile {public abstract LineRecord? ReadLine();public abstract void Rewind();public abstract void AppendLine(LineRecord record);public abstract void Close();}
public abstract class TextWorkspace {public abstract TextFile CreateFile();public abstract void DeleteFile(TextFile file);}
public class Solution
{
    public TextFile SortExternalFile(TextFile inputFile, int bufferLimit, TextWorkspace workspace)
    {
        inputFile.Rewind();
        var runs = new List<TextFile>();
        while (true)
        {
            var chunk = new List<LineRecord>();
            for (int i = 0; i < bufferLimit; ++i)
            {
                var record = inputFile.ReadLine();
                if (record is null)
                    break;
                chunk.Add(record);
            }
            if (chunk.Count == 0)
                break;
            chunk.Sort((first, second) => first.CompareTo(second));
            var run = workspace.CreateFile();
            foreach (var record in chunk)
                run.AppendLine(record);
            run.Close();
            runs.Add(run);
        }
        inputFile.Close();
        if (runs.Count == 0)
        {
            var empty = workspace.CreateFile();
            empty.Close();
            return empty;
        }
        while (runs.Count > 1)
        {
            var merged = new List<TextFile>();
            for (int index = 0; index < runs.Count; index += 2)
            {
                if (index + 1 == runs.Count)
                {
                    merged.Add(runs[index]);
                    continue;
                }
                var left = runs[index];
                var right = runs[index + 1];
                left.Rewind();
                right.Rewind();
                var output = workspace.CreateFile();
                LineRecord? first = left.ReadLine(), second = right.ReadLine();
                while (first is not null || second is not null)
                {
                    if (second is null || (first is not null && first.CompareTo(second) <= 0))
                    {
                        output.AppendLine(first!);
                        first = left.ReadLine();
                    }
                    else
                    {
                        output.AppendLine(second);
                        second = right.ReadLine();
                    }
                }
                output.Close();
                left.Close();
                right.Close();
                workspace.DeleteFile(left);
                workspace.DeleteFile(right);
                merged.Add(output);
            }
            runs = merged;
        }
        runs[0].Rewind();
        return runs[0];
    }
}
