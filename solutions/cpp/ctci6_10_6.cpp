#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
struct LineRecord {virtual int CompareTo(const LineRecord& other)const=0;virtual void Release()=0;protected:virtual ~LineRecord()=default;};
struct TextFile {virtual LineRecord* ReadLine()=0;virtual void Rewind()=0;virtual void AppendLine(LineRecord& record)=0;virtual void Close()=0;protected:virtual ~TextFile()=default;};
struct TextWorkspace {virtual TextFile* CreateFile()=0;virtual void DeleteFile(TextFile& file)=0;protected:virtual ~TextWorkspace()=default;};
class Solution {
 public:
  TextFile* SortExternalFile(TextFile& inputFile, int bufferLimit, TextWorkspace& workspace) {
    inputFile.Rewind();
    std::vector<TextFile*> runs;
    while (true) {
      std::vector<LineRecord*> chunk;
      for (int i = 0; i < bufferLimit; ++i) {
        auto record = inputFile.ReadLine();
        if (!record)
          break;
        chunk.push_back(record);
      }
      if (chunk.empty())
        break;
      std::sort(chunk.begin(), chunk.end(), [](LineRecord* first, LineRecord* second) {
        return first->CompareTo(*second) < 0;
      });
      TextFile* run = workspace.CreateFile();
      for (auto record : chunk)
        run->AppendLine(*record);
      run->Close();
      runs.push_back(run);
    }
    inputFile.Close();
    if (runs.empty()) {
      TextFile* empty = workspace.CreateFile();
      empty->Close();
      return empty;
    }
    while (runs.size() > 1) {
      std::vector<TextFile*> merged;
      for (std::size_t index = 0; index < runs.size(); index += 2) {
        if (index + 1 == runs.size()) {
          merged.push_back(runs[index]);
          continue;
        }
        TextFile* left = runs[index];
        TextFile* right = runs[index + 1];
        left->Rewind();
        right->Rewind();
        TextFile* output = workspace.CreateFile();
        LineRecord* first = left->ReadLine();
        LineRecord* second = right->ReadLine();
        while (first || second) {
          if (!second || (first && first->CompareTo(*second) <= 0)) {
            output->AppendLine(*first);
            first = left->ReadLine();
          } else {
            output->AppendLine(*second);
            second = right->ReadLine();
          }
        }
        output->Close();
        left->Close();
        right->Close();
        workspace.DeleteFile(*left);
        workspace.DeleteFile(*right);
        merged.push_back(output);
      }
      runs = std::move(merged);
    }
    runs[0]->Rewind();
    return runs[0];
  }
};
