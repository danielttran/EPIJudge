"""Compiled file-preservation, chronological-order and blank-line regressions."""
import hashlib,json,unittest
from core import ROOT,LANGUAGES,EXT
from models10 import declare
from tail12 import SPEC,BODIES
from verify01 import execute
from verify_runtime import core_match

class TailRuntimeTests(unittest.TestCase):
    def test_file_mutation_reverse_and_blank_sentinel_are_rejected(self):
        entry=next(e for e in json.loads((ROOT/'ctci6/runtime/catalog.json').read_text()) if e['ref']=='12.1')
        records=[]
        for language in LANGUAGES:
            base=BODIES[language]
            stop={
                'python':base.replace('suffix.append(line[:-1])','if not line[:-1]:\n            break\n        suffix.append(line[:-1])'),
                'javascript':base.replace('ring[next] = current;','if (current === "") return [];\n                ring[next] = current;'),
                'csharp':base.replace('suffix.Enqueue(line);','if (line.Length == 0) break;\n    suffix.Enqueue(line);'),
                'java':base.replace('suffix.addLast(line);','if (line.isEmpty()) break;\n        suffix.addLast(line);'),
                'cpp':base.replace('suffix.push_back(line);','if (line.empty()) break;\n    suffix.push_back(line);')}[language]
            # These use the same suffix algorithm, changing only the final observable obligation.
            returns={'python':'return list(suffix)','javascript':'return result;','csharp':'return new List<string>(suffix);','java':'return new ArrayList<>(suffix);','cpp':'return std::vector<std::string>(suffix.begin(), suffix.end());'}
            reversed_return={'python':'return list(reversed(suffix))','javascript':'return result.reverse();','csharp':'return suffix.Reverse().ToList();','java':'var answer=new ArrayList<>(suffix); Collections.reverse(answer); return answer;','cpp':'return std::vector<std::string>(suffix.rbegin(), suffix.rend());'}
            write={'python':'open(filePath, "w").close()\n','javascript':'tailFs.writeFileSync(filePath, "");\n','csharp':'System.IO.File.WriteAllText(filePath, "");\n','java':'try { java.nio.file.Files.writeString(java.nio.file.Path.of(filePath), ""); } catch(java.io.IOException error) { throw new java.io.UncheckedIOException(error); }\n','cpp':'std::ofstream(filePath, std::ios::trunc).close();\n'}
            reverse=base.replace(returns[language],reversed_return[language])
            mutate=base.replace(returns[language],write[language]+returns[language])
            case=dict(ref='12.1',arguments=SPEC['example'][0],expected=SPEC['example'][1])
            for label,algorithm in [('blank-sentinel',stop),('reverse',reverse),('input-write',mutate)]:
                with self.subTest(language=language,variant=label):
                    config=entry['languages'][language];_,code=declare(SPEC,language,algorithm)
                    filename=('Solution.' if language in ('csharp','java') else 'solution.')+EXT[language]
                    composed=config['prefix']+code+config['suffix']
                    rows=execute(language,False,[case],ROOT/'.epi-runs/ctci6-tail-negative'/language/label,source_builder=lambda *_:config['harness'],companion_files={filename:composed})
                    observed=rows[0]['observation'];self.assertNotIn('error',observed);self.assertFalse(core_match(case,observed))
                    if label=='input-write':self.assertEqual(observed['actual'],case['expected']);self.assertFalse(observed['mutationOk'])
                    records.append(dict(language=language,variant=label,fixtures=1,outcome='rejected',codeSha256=hashlib.sha256(composed.encode()).hexdigest(),harnessSha256=hashlib.sha256(config['harness'].encode()).hexdigest()))
        (ROOT/'ctci6/tail12-validation.json').write_text(json.dumps(dict(status='passed',reference='12.1',compiledPrograms=len(records),fixtures=len(records),executions=records),indent=2)+'\n')
if __name__=='__main__':unittest.main()
