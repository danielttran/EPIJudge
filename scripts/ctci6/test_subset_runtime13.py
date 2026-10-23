"""Compile distribution/mutation counterexamples and alternative fair filters."""
import json
import unittest
from core import ROOT,LANGUAGES,EXT
from chapter13 import SPECS
from algorithms13 import body
from models13 import declare
from corpus_subset13 import oracle,valid_observation
from verify01 import execute

class SubsetRuntimeTests(unittest.TestCase):
    def run_code(self,language,label,algorithm,arrays):
        entry=next(e for e in json.loads((ROOT/'ctci6/runtime/catalog.json').read_text()) if e['ref']=='13.8');config=entry['languages'][language];spec=next(s for s in SPECS if s['ref']=='13.8');_,code=declare(spec,language,algorithm)
        filename=('Solution.' if language in ('csharp','java') else 'solution.')+EXT[language]
        cases=[dict(ref='13.8',arguments=[a,[]],expected=oracle('13.8',[a,[]])) for a in arrays]
        results=execute(language,False,cases,ROOT/'.epi-runs/ctci6-subset13-variants'/language/label,source_builder=lambda *_:config['harness'],companion_files={filename:config['prefix']+code+config['suffix']})
        return cases,[r['observation'] for r in results]
    def test_shared_coin_distinct_values_and_input_reordering_are_rejected(self):
        shared={'python':'return values.copy() if coins.Next() else []','javascript':'return coins.Next()?values.slice():[];','csharp':'return coins.Next()?values.ToArray():[];','java':'return coins.Next()?values.clone():new int[0];','cpp':'return coins.Next()?values:std::vector<int>{};'}
        dedup={'python':'return list(filter(lambda value: coins.Next(), dict.fromkeys(values)))','javascript':'return [...new Set(values)].filter(value=>coins.Next());','csharp':'return values.Distinct().Where(value=>coins.Next()).ToArray();','java':'return Arrays.stream(values).distinct().filter(value->coins.Next()).toArray();','cpp':'std::vector<int> result,seen;for(int value:values)if(std::find(seen.begin(),seen.end(),value)==seen.end()){seen.push_back(value);if(coins.Next())result.push_back(value);}return result;'}
        reorder={'python':'values.reverse()\n','javascript':'values.reverse();','csharp':'Array.Reverse(values);','java':'for(int i=0;i<values.length/2;++i){int j=values.length-1-i,saved=values[i];values[i]=values[j];values[j]=saved;}','cpp':'auto& changed=const_cast<std::vector<int>&>(values);std::reverse(changed.begin(),changed.end());'}
        for language in LANGUAGES:
            for label,algorithm in [('shared-coin',shared[language]),('deduplicated',dedup[language]),('mutating',reorder[language]+body('13.8',language))]:
                with self.subTest(language=language,variant=label):
                    arrays=[[7,7,9],[9,7,7]] if label=='deduplicated' else [[1,2,3],[7,7,9]]
                    cases,observed=self.run_code(language,label,algorithm,arrays)
                    for case,value in zip(cases,observed):self.assertFalse(valid_observation('13.8',case,value));self.assertIn('error',value)
    def test_inverted_and_two_coin_xor_filters_are_valid(self):
        xor={'python':'return list(filter(lambda value: coins.Next() != coins.Next(),values))','javascript':'return values.filter(value=>coins.Next()!==coins.Next());','csharp':'return values.Where(value=>coins.Next()!=coins.Next()).ToArray();','java':'return Arrays.stream(values).filter(value->coins.Next()!=coins.Next()).toArray();','cpp':'std::vector<int> result;std::copy_if(values.begin(),values.end(),std::back_inserter(result),[&coins](int){bool first=coins.Next();bool second=coins.Next();return first!=second;});return result;'}
        for language in LANGUAGES:
            inverted=body('13.8',language).replace('coins.Next()','not coins.Next()' if language=='python' else '!coins.Next()')
            for label,algorithm in [('inverted',inverted),('two-coin-xor',xor[language])]:
                with self.subTest(language=language,variant=label):
                    cases,observed=self.run_code(language,label,algorithm,[[7,7,9],[7]*5])
                    for case,value in zip(cases,observed):self.assertNotIn('error',value);self.assertTrue(valid_observation('13.8',case,value))
if __name__=='__main__':unittest.main()
