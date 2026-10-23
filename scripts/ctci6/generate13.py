"""Preflight examples before generation and attach actual language WHY notes."""
import json
from algorithms13 import body
from chapter13 import SPECS
from core import LANGUAGES,ROOT
from corpus13 import cases,oracle
from generate import generate
from models13 import declare,header,neutral

def generate13():
    for spec in SPECS:
        assert oracle(spec['ref'],spec['example'][0])==spec['example'][1]
        cases(spec)
    rows=[]
    for spec in SPECS:
        generate(specs=[spec],algorithm=body,corpus=cases,reference=oracle,headers={l:header(spec['ref'],l) for l in LANGUAGES},declare=declare,neutral=neutral,staging_name='staged13')
        rows.extend(json.loads((ROOT/'ctci6/staged13/catalog.json').read_text()))
        for language,detail in spec['languageWhy'].items():
            path=ROOT/'ctci6/staged13'/language/('ctci6_'+spec['ref'].replace('.','_')+'.json');notes=json.loads(path.read_text());notes['explanation']+=' '+detail;path.write_text(json.dumps(notes,indent=2)+'\n')
    (ROOT/'ctci6/staged13/catalog.json').write_text(json.dumps(rows,indent=2)+'\n')
if __name__=='__main__':generate13()
