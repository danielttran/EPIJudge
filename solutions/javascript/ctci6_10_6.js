'use strict';
class LineRecord {CompareTo(other){throw new Error("Provided by the judge");}Release(){throw new Error("Provided by the judge");}}
class TextFile {ReadLine(){throw new Error("Provided by the judge");}Rewind(){throw new Error("Provided by the judge");}AppendLine(record){throw new Error("Provided by the judge");}Close(){throw new Error("Provided by the judge");}}
class TextWorkspace {CreateFile(){throw new Error("Provided by the judge");}DeleteFile(file){throw new Error("Provided by the judge");}}
function SortExternalFile(inputFile, bufferLimit, workspace) {
  inputFile.Rewind();
  let runs = [];
  while (true) {
    const chunk = [];
    for (let i = 0; i < bufferLimit; ++i) {
      const record = inputFile.ReadLine();
      if (record === null) break;
      chunk.push(record);
    }
    if (chunk.length === 0) break;
    chunk.sort((first, second) => first.CompareTo(second));
    const run = workspace.CreateFile();
    for (const record of chunk) run.AppendLine(record);
    run.Close();
    runs.push(run);
  }
  inputFile.Close();
  if (runs.length === 0) {
    const empty = workspace.CreateFile();
    empty.Close();
    return empty;
  }
  while (runs.length > 1) {
    const merged = [];
    for (let index = 0; index < runs.length; index += 2) {
      if (index + 1 === runs.length) {
        merged.push(runs[index]);
        continue;
      }
      const left = runs[index],
        right = runs[index + 1];
      left.Rewind();
      right.Rewind();
      const output = workspace.CreateFile();
      let first = left.ReadLine(),
        second = right.ReadLine();
      while (first !== null || second !== null) {
        if (second === null || (first !== null && first.CompareTo(second) <= 0)) {
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
      merged.push(output);
    }
    runs = merged;
  }
  runs[0].Rewind();
  return runs[0];
}

module.exports = {LineRecord,TextFile,TextWorkspace,SortExternalFile};
