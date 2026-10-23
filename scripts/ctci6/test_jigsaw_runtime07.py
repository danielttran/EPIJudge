"""Execute invalid indices, forbidden input writes and alternative valid assemblies."""
import json,unittest
from algorithms_jigsaw07 import body
from chapter07 import SPECS
from core import ROOT,LANGUAGES,EXT
from corpus_jigsaw07 import oracle,valid_observation
from models07 import declare
from verify01 import execute

class JigsawRuntimeTests(unittest.TestCase):
    def test_actual_programs_and_alternative_order(self):
        entry=next(e for e in json.loads((ROOT/'ctci6/runtime/catalog.json').read_text()) if e['ref']=='7.6')
        spec=next(s for s in SPECS if s['ref']=='7.6');args=spec['example'][0]
        for language in LANGUAGES:
            duplicate={'python':'return [[0,0] for _ in pieces]','javascript':'return pieces.map(()=>[0,0]);','cpp':'return std::vector<std::vector<int>>(pieces.size(),{0,0});','csharp':'return pieces.Select(_=>new int[]{0,0}).ToArray();','java':'return new int[][]{{0,0},{0,0},{0,0},{0,0}};'}[language]
            mutate={'python':'pieces[0][0]=99\nreturn [[0,0],[1,0],[2,0],[3,0]]','javascript':'pieces[0][0]=99;return [[0,0],[1,0],[2,0],[3,0]];','cpp':'const_cast<std::vector<std::vector<int>>&>(pieces)[0][0]=99;return {{0,0},{1,0},{2,0},{3,0}};','csharp':'pieces[0][0]=99;return new int[][]{new[]{0,0},new[]{1,0},new[]{2,0},new[]{3,0}};','java':'pieces[0][0]=99;return new int[][]{{0,0},{1,0},{2,0},{3,0}};'}[language]
            original=body(language)
            reverse=original.replace('for index in range(count):','for index in range(count-1,-1,-1):').replace('for(let index=0;index<count;++index)','for(let index=count-1;index>=0;--index)').replace('for(int index=0;index<count;++index)','for(int index=count-1;index>=0;--index)')
            self.assertNotEqual(original,reverse)
            for variant,algorithm in (('duplicate',duplicate),('mutation',mutate),('reverse-search',reverse)):
                with self.subTest(language=language,variant=variant):
                    config=entry['languages'][language];_,code=declare(spec,language,algorithm)
                    cases=[dict(ref='7.6',arguments=args,expected=oracle('7.6',args))]
                    filename=('Solution.' if language in ('java','csharp') else 'solution.')+EXT[language]
                    rows=execute(language,False,cases,ROOT/'.epi-runs/ctci6-jigsaw7-variants'/language/variant,source_builder=lambda *_:config['harness'],companion_files={filename:config['prefix']+code+config['suffix']})
                    self.assertEqual(valid_observation('7.6',cases[0],rows[0]['observation']),variant=='reverse-search')
                    if variant=='reverse-search':self.assertNotEqual(rows[0]['observation']['actual'],cases[0]['expected'])
if __name__=='__main__':unittest.main()
