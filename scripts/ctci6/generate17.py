"""Generate a frozen reviewed batch through existing local formatting paths."""
from algorithms17 import body
from chapter17 import SPECS
from core import LANGUAGES
from core import ROOT
import json
from corpus17 import cases as base_cases,oracle as base_oracle
import corpus_names17

import corpus_numeric
import corpus_bits17
import corpus_binode17
import corpus_random17

def cases(spec):return corpus_random17.cases(spec) if spec["ref"] in ("17.2","17.3") else corpus_binode17.cases(spec) if spec["ref"]=="17.12" else corpus_bits17.cases(spec) if spec["ref"]=="17.4" else corpus_numeric.cases(spec) if spec["ref"]=="17.20" else corpus_names17.cases(spec) if spec["ref"]=="17.7" else base_cases(spec)
def oracle(reference,args):return corpus_random17.oracle(reference,args) if reference in ("17.2","17.3") else corpus_binode17.oracle(reference,args) if reference=="17.12" else corpus_bits17.oracle(reference,args) if reference=="17.4" else corpus_numeric.oracle(reference,args) if reference=="17.20" else corpus_names17.oracle(reference,args) if reference=="17.7" else base_oracle(reference,args)
from generate import generate
from models17 import declare,header,neutral

def generate17():
    for spec in SPECS:
        if oracle(spec['ref'],spec['example'][0])!=spec['example'][1]:raise ValueError('Incorrect example '+spec['ref'])
        cases(spec)
    rows=[]
    for spec in SPECS:
        generate(specs=[spec],algorithm=body,corpus=cases,reference=oracle,headers={language:header(spec['ref'],language) for language in LANGUAGES},declare=declare,neutral=neutral,staging_name='staged17')
        rows.extend(json.loads((ROOT/'ctci6/staged17/catalog.json').read_text()))
    (ROOT/'ctci6/staged17/catalog.json').write_text(json.dumps(rows,indent=2)+'\n')
    for spec in SPECS:
        for language, detail in spec.get('languageWhy', {}).items():
            path = ROOT / 'ctci6/staged17' / language / ('ctci6_' + spec['ref'].replace('.', '_') + '.json')
            notes = json.loads(path.read_text())
            notes['explanation'] += ' ' + detail
            path.write_text(json.dumps(notes, indent=2) + '\n')

if __name__=='__main__':generate17()
