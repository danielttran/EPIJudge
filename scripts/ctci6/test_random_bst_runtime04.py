"""Compile physical-node probability/identity mutants and valid cache-free queries."""
import json
import unittest
from algorithms_random04 import body
from core import ROOT,LANGUAGES,EXT
from corpus_random04 import transcript,oracle,valid_observation
from verify01 import execute

BFS={
'python':'''if self.Root is None:
    return None
nodes=[self.Root]
for node in nodes:
    if node.Left is not None:nodes.append(node.Left)
    if node.Right is not None:nodes.append(node.Right)
return nodes[RandomSource.GetRandom(0,len(nodes)-1)]''',
'javascript':'''if(this.Root===null)return null;const nodes=[this.Root];for(let i=0;i<nodes.length;++i){if(nodes[i].Left!==null)nodes.push(nodes[i].Left);if(nodes[i].Right!==null)nodes.push(nodes[i].Right);}return nodes[RandomSource.GetRandom(0,nodes.length-1)];''',
'csharp':'''if(Root is null)return null;var nodes=new List<RandomNode>{Root};for(int i=0;i<nodes.Count;++i){if(nodes[i].Left is not null)nodes.Add(nodes[i].Left!);if(nodes[i].Right is not null)nodes.Add(nodes[i].Right!);}return nodes[RandomSource.GetRandom(0,nodes.Count-1)];''',
'java':'''if(Root==null)return null;var nodes=new ArrayList<RandomNode>();nodes.add(Root);for(int i=0;i<nodes.size();++i){if(nodes.get(i).Left!=null)nodes.add(nodes.get(i).Left);if(nodes.get(i).Right!=null)nodes.add(nodes.get(i).Right);}return nodes.get(RandomSource.GetRandom(0,nodes.size()-1));''',
'cpp':'''if(!Root)return nullptr;std::vector<RandomNode*> nodes{Root};for(size_t i=0;i<nodes.size();++i){if(nodes[i]->Left)nodes.push_back(nodes[i]->Left);if(nodes[i]->Right)nodes.push_back(nodes[i]->Right);}return nodes[RandomSource::GetRandom(0,static_cast<int>(nodes.size())-1)];'''}
def replace_method(code,language,name,replacement):
    if language=='python':
        start=code.index('\n    def '+name+'(');end=code.find('\n    def ',start+1)
        if end<0:end=len(code)
        signature=code[start:code.index('\n',start+1)]
        return code[:start]+signature+'\n'+'\n'.join('        '+line for line in replacement.splitlines())+'\n'+code[end:]
    start=code.index(name+'(');opening=code.index('{',start);depth=1;end=opening+1
    while depth:
        depth+=(code[end]=='{')-(code[end]=='}');end+=1
    return code[:opening+1]+replacement+code[end-1:]

class RandomBstRuntimeTests(unittest.TestCase):
    def run_code(self,language,label,code,actions):
        entry=next(e for e in json.loads((ROOT/'ctci6/runtime/catalog.json').read_text()) if e['ref']=='4.11');config=entry['languages'][language]
        filename='RandomBst.java' if language=='java' else ('Solution.' if language=='csharp' else 'solution.')+EXT[language]
        cases=[dict(ref='4.11',arguments=transcript(a),expected=oracle('4.11',transcript(a))) for a in actions]
        results=execute(language,False,cases,ROOT/'.epi-runs/ctci6-random-bst'/language/label,source_builder=lambda *_:config['harness'],companion_files={filename:config['prefix']+code+config['suffix']})
        return cases,[r['observation'] for r in results]
    def test_cache_free_bfs_query_is_valid(self):
        for language in LANGUAGES:
            with self.subTest(language=language):
                prefix='RandomSource.GetRandom(2147483647,2147483647)\nRandomSource.GetRandom(0,2147483647)\n' if language=='python' else 'RandomSource::GetRandom(2147483647,2147483647);RandomSource::GetRandom(0,2147483647);' if language=='cpp' else 'RandomSource.GetRandom(2147483647,2147483647);RandomSource.GetRandom(0,2147483647);'
                code=replace_method(body(language),language,'GetRandomNode',prefix+BFS[language])
                cases,observed=self.run_code(language,'valid-bfs',code,[[('GetRandomNode',None)],[('Insert',7),('Insert',7),('Insert',9),('GetRandomNode',None),('Delete',7),('GetRandomNode',None)]])
                for case,value in zip(cases,observed):self.assertNotIn('error',value);self.assertTrue(valid_observation('4.11',case,value))
    def test_collapsed_duplicate_identity_clone_and_noop_delete_fail(self):
        for language in LANGUAGES:
            with self.subTest(language=language):
                getter=BFS[language]
                if language=='python':getter=getter.replace('return nodes[RandomSource.GetRandom(0,len(nodes)-1)]','return self.Find(nodes[RandomSource.GetRandom(0,len(nodes)-1)].Data)')
                elif language=='javascript':getter=getter.replace('return nodes[RandomSource.GetRandom(0,nodes.length-1)];','return this.Find(nodes[RandomSource.GetRandom(0,nodes.length-1)].Data);')
                elif language=='csharp':getter=getter.replace('return nodes[RandomSource.GetRandom(0,nodes.Count-1)];','return Find(nodes[RandomSource.GetRandom(0,nodes.Count-1)].Data);')
                elif language=='java':getter=getter.replace('return nodes.get(RandomSource.GetRandom(0,nodes.size()-1));','return Find(nodes.get(RandomSource.GetRandom(0,nodes.size()-1)).Data);')
                else:getter=getter.replace('return nodes[RandomSource::GetRandom(0,static_cast<int>(nodes.size())-1)];','return Find(nodes[RandomSource::GetRandom(0,static_cast<int>(nodes.size())-1)]->Data);')
                code=replace_method(body(language),language,'GetRandomNode',getter)
                cases,observed=self.run_code(language,'collapsed-duplicates',code,[[('Insert',7),('Insert',7),('Insert',9),('GetRandomNode',None)]])
                self.assertFalse(valid_observation('4.11',cases[0],observed[0]));self.assertRegex(observed[0].get('error','').lower(),r'bias|permutation')
                clone='return RandomNode(value)' if language=='python' else 'return new RandomNode(value);'
                code=replace_method(body(language),language,'Find',clone)
                code=replace_method(code,language,'Delete','return True' if language=='python' else 'return true;')
                cases,observed=self.run_code(language,'clone-and-noop-delete',code,[[('Insert',7),('Find',7)],[('Insert',7),('Delete',7)]])
                for case,value in zip(cases,observed):self.assertFalse(valid_observation('4.11',case,value))
                self.assertRegex(observed[0].get('error','').lower(),r'current (tree )?node')
if __name__=='__main__':unittest.main()
