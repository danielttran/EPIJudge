class LineRecord:
    def CompareTo(self,other: "LineRecord") -> int:
        raise RuntimeError("Provided by the judge")
    def Release(self) -> None:
        raise RuntimeError("Provided by the judge")
class TextFile:
    def ReadLine(self) -> LineRecord | None:
        raise RuntimeError("Provided by the judge")
    def Rewind(self) -> None:
        raise RuntimeError("Provided by the judge")
    def AppendLine(self,record: LineRecord) -> None:
        raise RuntimeError("Provided by the judge")
    def Close(self) -> None:
        raise RuntimeError("Provided by the judge")
class TextWorkspace:
    def CreateFile(self) -> TextFile:
        raise RuntimeError("Provided by the judge")
    def DeleteFile(self,file: TextFile) -> None:
        raise RuntimeError("Provided by the judge")
def SortExternalFile(inputFile: TextFile, bufferLimit: int, workspace: TextWorkspace) -> TextFile:
    from functools import cmp_to_key

    inputFile.Rewind()
    runs = []
    while True:
        chunk = []
        for _ in range(bufferLimit):
            record = inputFile.ReadLine()
            if record is None:
                break
            chunk.append(record)
        if not chunk:
            break
        chunk.sort(key=cmp_to_key(lambda first, second: first.CompareTo(second)))
        run = workspace.CreateFile()
        for record in chunk:
            run.AppendLine(record)
        run.Close()
        runs.append(run)
    inputFile.Close()
    if not runs:
        empty = workspace.CreateFile()
        empty.Close()
        return empty
    while len(runs) > 1:
        merged = []
        for index in range(0, len(runs), 2):
            if index + 1 == len(runs):
                merged.append(runs[index])
                continue
            left, right = runs[index], runs[index + 1]
            left.Rewind()
            right.Rewind()
            output = workspace.CreateFile()
            first, second = left.ReadLine(), right.ReadLine()
            while first is not None or second is not None:
                if second is None or first is not None and first.CompareTo(second) <= 0:
                    output.AppendLine(first)
                    first = left.ReadLine()
                else:
                    output.AppendLine(second)
                    second = right.ReadLine()
            output.Close()
            left.Close()
            right.Close()
            workspace.DeleteFile(left)
            workspace.DeleteFile(right)
            merged.append(output)
        runs = merged
    runs[0].Rewind()
    return runs[0]
