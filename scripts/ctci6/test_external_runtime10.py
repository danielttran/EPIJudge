"""Execute resource/ownership violations and valid alternative external sorts."""
import json
import unittest
from algorithms_external10 import body
from chapter10 import SPECS
from core import ROOT,LANGUAGES,EXT
from corpus_external10 import oracle,valid_observation
from models10 import declare
from verify01 import execute

FAKE={
'python':'class FakeExternal10(TextFile):\n    def ReadLine(self):return None\n    def Rewind(self):pass\n    def AppendLine(self,record):record.Release()\n    def Close(self):pass\n',
'javascript':'class FakeExternal10 extends TextFile{ReadLine(){return null;}Rewind(){}AppendLine(record){record.Release();}Close(){}}\n',
'csharp':'sealed class FakeExternal10:TextFile{public override LineRecord? ReadLine()=>null;public override void Rewind(){}public override void AppendLine(LineRecord record){record.Release();}public override void Close(){}}\n',
'java':'class FakeExternal10 extends TextFile{public LineRecord ReadLine(){return null;}public void Rewind(){}public void AppendLine(LineRecord record){record.Release();}public void Close(){}}\n',
'cpp':'struct FakeExternal10:TextFile{LineRecord* ReadLine()override{return nullptr;}void Rewind()override{}void AppendLine(LineRecord& record)override{record.Release();}void Close()override{}~FakeExternal10()override=default;};\n'}
def negative(language,label):
    if language=='python':
        return {
'buffer-all':'from functools import cmp_to_key\nall_records=[]\nwhile True:\n    record=inputFile.ReadLine()\n    if record is None:break\n    all_records.append(record)\nall_records.sort(key=cmp_to_key(lambda a,b:a.CompareTo(b)))\noutput=workspace.CreateFile()\nfor record in all_records:output.AppendLine(record)\nreturn output',
'reuse':'record=inputFile.ReadLine()\noutput=workspace.CreateFile()\noutput.AppendLine(record)\noutput.AppendLine(record)\nreturn output',
'input-write':'record=inputFile.ReadLine()\ninputFile.AppendLine(record)\nreturn inputFile',
'foreign':'return FakeExternal10()',
'deleted':'output=workspace.CreateFile()\nworkspace.DeleteFile(output)\nreturn output',
'leak':'record=inputFile.ReadLine()\nreturn inputFile',
'eof-loop':'while True:\n    inputFile.ReadLine()',
'open-streams':'for _ in range(20):\n    record=inputFile.ReadLine()\n    output=workspace.CreateFile()\n    output.AppendLine(record)\nreturn inputFile'}[label]
    if language=='javascript':
        return {
'buffer-all':'const records=[];while(true){const record=inputFile.ReadLine();if(record===null)break;records.push(record);}records.sort((a,b)=>a.CompareTo(b));const output=workspace.CreateFile();for(const record of records)output.AppendLine(record);return output;',
'reuse':'const record=inputFile.ReadLine(),output=workspace.CreateFile();output.AppendLine(record);output.AppendLine(record);return output;',
'input-write':'const record=inputFile.ReadLine();inputFile.AppendLine(record);return inputFile;',
'foreign':'return new FakeExternal10();',
'deleted':'const output=workspace.CreateFile();workspace.DeleteFile(output);return output;',
'leak':'const record=inputFile.ReadLine();return inputFile;',
'eof-loop':'while(true)inputFile.ReadLine();',
'open-streams':'for(let i=0;i<20;++i){const record=inputFile.ReadLine(),output=workspace.CreateFile();output.AppendLine(record);}return inputFile;'}[label]
    if language=='cpp':
        return {
'buffer-all':'std::vector<LineRecord*> records;while(auto record=inputFile.ReadLine())records.push_back(record);std::sort(records.begin(),records.end(),[](LineRecord* a,LineRecord* b){return a->CompareTo(*b)<0;});auto output=workspace.CreateFile();for(auto record:records)output->AppendLine(*record);return output;',
'reuse':'auto record=inputFile.ReadLine();auto output=workspace.CreateFile();output->AppendLine(*record);output->AppendLine(*record);return output;',
'input-write':'auto record=inputFile.ReadLine();inputFile.AppendLine(*record);return &inputFile;',
'foreign':'static FakeExternal10 file;return &file;',
'deleted':'auto output=workspace.CreateFile();workspace.DeleteFile(*output);return output;',
'leak':'auto record=inputFile.ReadLine();return &inputFile;',
'eof-loop':'while(true)inputFile.ReadLine();',
'open-streams':'for(int i=0;i<20;++i){auto record=inputFile.ReadLine();auto output=workspace.CreateFile();output->AppendLine(*record);}return &inputFile;'}[label]
    java=language=='java';prefix='var ';records='new ArrayList<LineRecord>()' if java else 'new List<LineRecord>()';add='add' if java else 'Add';sort='records.sort((a,b)->a.CompareTo(b));' if java else 'records.Sort((a,b)=>a.CompareTo(b));';loop='for(var record:records)' if java else 'foreach(var record in records)'
    return {
'buffer-all':prefix+'records='+records+';while(true){var record=inputFile.ReadLine();if(record==null)break;records.'+add+'(record);}'+sort+'var output=workspace.CreateFile();'+loop+'output.AppendLine(record);return output;',
'reuse':'var record=inputFile.ReadLine();var output=workspace.CreateFile();output.AppendLine(record'+('' if java else '!')+');output.AppendLine(record'+('' if java else '!')+');return output;',
'input-write':'var record=inputFile.ReadLine();inputFile.AppendLine(record'+('' if java else '!')+');return inputFile;',
'foreign':'return new FakeExternal10();',
'deleted':'var output=workspace.CreateFile();workspace.DeleteFile(output);return output;',
'leak':'var record=inputFile.ReadLine();return inputFile;',
'eof-loop':'while(true)inputFile.ReadLine();',
'open-streams':'for(int i=0;i<20;++i){var record=inputFile.ReadLine();var output=workspace.CreateFile();output.AppendLine(record'+('' if java else '!')+');}return inputFile;'}[label]

class ExternalRuntimeTests(unittest.TestCase):
    def run_code(self,language,label,algorithm,args,prefix=''):
        entry=next(e for e in json.loads((ROOT/'ctci6/runtime/catalog.json').read_text()) if e['ref']=='10.6');config=entry['languages'][language];spec=next(s for s in SPECS if s['ref']=='10.6');_,code=declare(spec,language,algorithm)
        filename=('Solution.' if language in ('csharp','java') else 'solution.')+EXT[language]
        cases=[dict(ref='10.6',arguments=a,expected=oracle('10.6',a)) for a in args]
        rows=execute(language,False,cases,ROOT/'.epi-runs/ctci6-external10-variants'/language/label,source_builder=lambda *_:config['harness'],companion_files={filename:config['prefix']+prefix+code+config['suffix']})
        return cases,[r['observation'] for r in rows]
    def test_resource_and_ownership_violations_are_rejected(self):
        examples={'buffer-all':[['d','c','b','a'],2,[]],'reuse':[['one'],2,[]],'input-write':[['one'],2,[]],'foreign':[[],2,[]],'deleted':[[],2,[]],'leak':[['one'],2,[]],'eof-loop':[[],2,[]],'open-streams':[[str(i) for i in range(20)],2,[]]}
        messages={'buffer-all':'buffer limit','reuse':'consumed','input-write':'read-only','foreign':'live input/workspace','deleted':'live input/workspace','leak':'release every record','eof-loop':'I/O budget','open-streams':'streams'}
        for language in LANGUAGES:
            for label,args in examples.items():
                with self.subTest(language=language,variant=label):
                    cases,observed=self.run_code(language,label,negative(language,label),[args],FAKE[language] if label=='foreign' else '')
                    self.assertFalse(valid_observation('10.6',cases[0],observed[0]));self.assertIn(messages[label],observed[0].get('error',''))
    def test_one_record_runs_and_right_ties_are_valid(self):
        for language in LANGUAGES:
            original=body(language)
            for label,code in [('one-record-runs',original.replace('range(bufferLimit)','range(1)').replace('i<bufferLimit','i<1')),('right-ties',original.replace('first.CompareTo(second)<=0','first.CompareTo(second)<0').replace('first->CompareTo(*second)<=0','first->CompareTo(*second)<0'))]:
                with self.subTest(language=language,variant=label):
                    self.assertNotEqual(original,code)
                    cases,observed=self.run_code(language,label,code,[[['z','','a','z',' A','a','!'],2,[]],[['same','same','','same',' '],8,[]]])
                    for case,value in zip(cases,observed):self.assertNotIn('error',value);self.assertTrue(valid_observation('10.6',case,value))
if __name__=='__main__':unittest.main()
