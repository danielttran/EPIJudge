"""Compile biased/mutating submissions and valid composition/order alternatives."""
import json
import unittest
from algorithms17 import body
from chapter17 import SPECS
from core import ROOT,LANGUAGES,EXT
from corpus_random17 import oracle,valid_observation
from models17 import declare
from verify01 import execute

class RandomCollectionRuntimeTests(unittest.TestCase):
    def run_code(self,ref,language,kind,code,args,field=None,global_prefix=""):
        entry=next(e for e in json.loads((ROOT/'ctci6/runtime/catalog.json').read_text()) if e['ref']==ref);spec=next(e for e in SPECS if e['ref']==ref);config=entry['languages'][language]
        _,code=declare(spec,language,code)
        if field is not None:
            self.assertIn("class Solution {",code);code=code.replace("class Solution {","class Solution {"+field,1)
        code=global_prefix+code
        filename=('Solution.' if language in ('csharp','java') else 'solution.')+EXT[language]
        cases=[dict(ref=ref,arguments=a,expected=oracle(ref,a)) for a in args]
        results=execute(language,False,cases,ROOT/'.epi-runs/ctci6-random-collections'/language/kind,source_builder=lambda *_:config['harness'],companion_files={filename:config['prefix']+code+config['suffix']})
        return cases,[r['observation'] for r in results]
    def test_fixed_shuffle_and_distinct_value_bias_or_input_mutation_fail(self):
        fixed={
          'python':'if len(values)>1:\n    RandomSource.GetRandom(0,len(values)-1)\nvalues.reverse()',
          'javascript':'if(values.length>1)RandomSource.GetRandom(0,values.length-1);values.reverse();',
          'csharp':'if(values.Length>1)RandomSource.GetRandom(0,values.Length-1);Array.Reverse(values);',
          'java':'if(values.length>1)RandomSource.GetRandom(0,values.length-1);for(int i=0;i<values.length/2;++i){int j=values.length-1-i,saved=values[i];values[i]=values[j];values[j]=saved;}',
          'cpp':'if(values.size()>1)RandomSource::GetRandom(0,static_cast<int>(values.size())-1);std::reverse(values.begin(),values.end());'}
        broken={
          'python':'if values[0] == 7:\n    return [7 if RandomSource.GetRandom(0,1)==0 else 9]\nvalues[0]=123\nreturn values[:count]',
          'javascript':'if(values[0]===7)return [RandomSource.GetRandom(0,1)===0?7:9];values[0]=123;return values.slice(0,count);',
          'csharp':'if(values[0]==7)return [RandomSource.GetRandom(0,1)==0?7:9];values[0]=123;return values.Take(count).ToArray();',
          'java':'if(values[0]==7)return new int[]{RandomSource.GetRandom(0,1)==0?7:9};values[0]=123;return Arrays.copyOf(values,count);',
          'cpp':'if(values[0]==7)return {RandomSource::GetRandom(0,1)==0?7:9};const_cast<std::vector<int>&>(values)[0]=123;return std::vector<int>(values.begin(),values.begin()+count);'}
        for language in LANGUAGES:
            with self.subTest(language=language):
                empty='if not values:\n    RandomSource.GetRandom(0,0)\n    return\n' if language=='python' else 'if(values.length===0){RandomSource.GetRandom(0,0);return;}' if language=='javascript' else 'if(values.Length==0){RandomSource.GetRandom(0,0);return;}' if language=='csharp' else 'if(values.length==0){RandomSource.GetRandom(0,0);return;}' if language=='java' else 'if(values.empty()){RandomSource::GetRandom(0,0);return;}'
                cases,observed=self.run_code('17.2',language,'fixed-shuffle',empty+fixed[language],[[[]],[[1,2,3]]])
                for case,value in zip(cases,observed):self.assertFalse(valid_observation('17.2',case,value))
                self.assertIn('bounds',observed[0].get('error','').lower())
                cases,observed=self.run_code('17.3',language,'biased-or-mutating-subset',broken[language],[[[7,7,9],1],[[1,2,3],1]])
                for case,value in zip(cases,observed):self.assertFalse(valid_observation('17.3',case,value))
                self.assertIn('bias',observed[0].get('error','').lower())
                self.assertIn('preserve input',observed[1].get('error','').lower())
    def test_double_shuffle_and_sorted_subset_are_valid(self):
        sorting={'python':'reservoir.sort()\nreturn reservoir','javascript':'reservoir.sort((a,b)=>a-b);return reservoir;','csharp':'Array.Sort(reservoir);return reservoir;','java':'Arrays.sort(reservoir);return reservoir;','cpp':'std::sort(reservoir.begin(),reservoir.end());return reservoir;'}
        for language in LANGUAGES:
            with self.subTest(language=language):
                original=body('17.2',language)
                code='for pass_index in range(2):\n'+'\n'.join('    '+line for line in original.splitlines()) if language=='python' else ('for(let passIndex=0;passIndex<2;++passIndex){' if language=='javascript' else 'for(int passIndex=0;passIndex<2;++passIndex){')+original+'}'
                cases,observed=self.run_code('17.2',language,'double-shuffle',code,[[[1,2,3]],[[5]*5]])
                for case,value in zip(cases,observed):self.assertNotIn('error',value);self.assertTrue(valid_observation('17.2',case,value))
                original=body('17.3',language);marker='return reservoir' if language=='python' else 'return reservoir;';prefix,suffix=original.rsplit(marker,1);code=prefix+sorting[language]+suffix
                cases,observed=self.run_code('17.3',language,'sorted-subset',code,[[[7,7,9],1],[[7,7,9,1,2],3]])
                for case,value in zip(cases,observed):self.assertNotIn('error',value);self.assertTrue(valid_observation('17.3',case,value))

    def test_uniform_marginals_do_not_allow_correlated_rotation_cycles(self):
        bodies={
          'python':'global _cycle_cursor\nRandomSource.GetRandom(0,len(values)-1)\nshift = _cycle_cursor % len(values)\n_cycle_cursor += 1\nvalues[:] = values[shift:]+values[:shift]',
          'javascript':'RandomSource.GetRandom(0,values.length-1);const shift=cycleCursor++%values.length,copy=values.slice();for(let i=0;i<values.length;++i)values[i]=copy[(i+shift)%values.length];',
          'csharp':'RandomSource.GetRandom(0,values.Length-1);int shift=cycleCursor++%values.Length;var copy=values.ToArray();for(int i=0;i<values.Length;++i)values[i]=copy[(i+shift)%values.Length];',
          'java':'RandomSource.GetRandom(0,values.length-1);int shift=cycleCursor++%values.length;int[] copy=values.clone();for(int i=0;i<values.length;++i)values[i]=copy[(i+shift)%values.length];',
          'cpp':'RandomSource::GetRandom(0,static_cast<int>(values.size())-1);int shift=cycleCursor++%static_cast<int>(values.size());auto copy=values;for(size_t i=0;i<values.size();++i)values[i]=copy[(i+shift)%values.size()];'}
        for language in LANGUAGES:
            with self.subTest(language=language):
                field=None if language in ('python','javascript') else 'private int cycleCursor;' if language in ('csharp','java') else 'int cycleCursor=0;'
                prefix='_cycle_cursor=0\n' if language=='python' else 'let cycleCursor=0;\n' if language=='javascript' else ''
                cases,observed=self.run_code('17.2',language,'correlated-cycle',bodies[language],[[list(range(6))]],field,prefix)
                self.assertFalse(valid_observation('17.2',cases[0],observed[0]));self.assertIn('correlated',observed[0].get('error','').lower())

if __name__=='__main__':unittest.main()
