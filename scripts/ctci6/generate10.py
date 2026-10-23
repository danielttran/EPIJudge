"""Generate a frozen reviewed batch through existing local formatting paths."""
from algorithms10 import body
from chapter10 import SPECS
from core import LANGUAGES
from core import ROOT
import json
from corpus10 import cases,oracle
from generate import generate
from models10 import declare,header,neutral

def generate10():
    for spec in SPECS:
        if oracle(spec['ref'],spec['example'][0])!=spec['example'][1]:raise ValueError('Incorrect example '+spec['ref'])
        cases(spec)
    rows = []
    for spec in SPECS:
        generate(specs=[spec],algorithm=body,corpus=cases,reference=oracle,headers={language:header(spec['ref'],language) for language in LANGUAGES},declare=declare,neutral=neutral,staging_name='staged10')
        rows.extend(json.loads((ROOT / 'ctci6/staged10/catalog.json').read_text()))
    (ROOT / 'ctci6/staged10/catalog.json').write_text(json.dumps(rows,indent=2)+'\n')
    for spec in SPECS:
        for language, detail in spec.get('languageWhy', {}).items():
            path = ROOT / 'ctci6/staged10' / language / ('ctci6_' + spec['ref'].replace('.', '_') + '.json')
            notes = json.loads(path.read_text())
            notes['explanation'] += ' ' + detail
            path.write_text(json.dumps(notes, indent=2) + '\n')

if __name__=='__main__':generate10()
