"""Compile readonly-input and missing-filter regressions in all languages."""
import json
import unittest
from core import ROOT,LANGUAGES,EXT
from chapter13 import SPECS
from algorithms13 import body
from models13 import declare
from corpus13 import valid_observation
from verify01 import execute

class CountryRuntimeTests(unittest.TestCase):
    def test_input_reordering_and_unfiltered_totals_are_rejected(self):
        entry=next(e for e in json.loads((ROOT/'ctci6/runtime/catalog.json').read_text()) if e['ref']=='13.7');spec=SPECS[0]
        mutations={'python':'countries.reverse()\n','javascript':'countries.reverse();','csharp':'Array.Reverse(countries);','java':'Collections.reverse(Arrays.asList(countries));','cpp':'auto& mutableCountries=const_cast<std::vector<Country>&>(countries);std::reverse(mutableCountries.begin(),mutableCountries.end());'}
        wrong={'python':'return sum(country.GetPopulation() for country in countries)','javascript':'return countries.reduce((sum,country)=>sum+country.GetPopulation(),0);','csharp':'return countries.Sum(country=>country.GetPopulation());','java':'return Arrays.stream(countries).mapToInt(country->country.GetPopulation()).sum();','cpp':'return std::accumulate(countries.begin(),countries.end(),0,[](int sum,const Country& country){return sum+country.GetPopulation();});'}
        case=dict(ref='13.7',arguments=spec['example'][0],expected=spec['example'][1])
        for language in LANGUAGES:
            for label,algorithm in [('reorder',mutations[language]+body('13.7',language)),('ignore-filter',wrong[language])]:
                with self.subTest(language=language,variant=label):
                    config=entry['languages'][language];_,code=declare(spec,language,algorithm)
                    filename=('Solution.' if language in ('csharp','java') else 'solution.')+EXT[language]
                    rows=execute(language,False,[case],ROOT/'.epi-runs/ctci6-country-negative'/language/label,source_builder=lambda *_:config['harness'],companion_files={filename:config['prefix']+code+config['suffix']})
                    observed=rows[0]['observation'];self.assertNotIn('error',observed);self.assertFalse(valid_observation('13.7',case,observed))
                    if label=='reorder':self.assertEqual(case['expected'],observed['actual']);self.assertFalse(observed['mutationOk'])
if __name__=='__main__':unittest.main()
