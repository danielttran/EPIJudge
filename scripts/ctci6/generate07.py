"""Preflight independent state traces before generating generic state classes."""
import json
from algorithms07 import body
from chapter07 import SPECS
from core import ROOT,LANGUAGES
from corpus07 import cases,oracle
from generate import generate
from models07 import declare,header,neutral

def generate07():
    for spec in SPECS:
        assert oracle(spec['ref'],spec['example'][0])==spec['example'][1]
        cases(spec)
    rows=[]
    for spec in SPECS:
        generate(specs=[spec],algorithm=body,corpus=cases,reference=oracle,headers={language:header(spec['ref'],language) for language in LANGUAGES},declare=declare,neutral=neutral,staging_name='staged07')
        rows.extend(json.loads((ROOT/'ctci6/staged07/catalog.json').read_text()))
        for language,detail in spec['languageWhy'].items():
            path=ROOT/'ctci6/staged07'/language/('ctci6_'+spec['ref'].replace('.','_')+'.json');notes=json.loads(path.read_text());notes['explanation']+=' '+detail;path.write_text(json.dumps(notes,indent=2)+'\n')
    (ROOT/'ctci6/staged07/catalog.json').write_text(json.dumps(rows,indent=2)+'\n')
if __name__=='__main__':generate07()
