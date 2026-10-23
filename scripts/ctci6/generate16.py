"""Generate a frozen reviewed batch through existing local formatting paths."""
from algorithms16 import body
from chapter16 import SPECS
from core import LANGUAGES,ROOT
import json
from corpus16 import cases as base_cases,oracle as base_oracle
import corpus_line16

def cases(spec):return corpus_line16.cases(spec) if spec["ref"]=="16.14" else base_cases(spec)
def oracle(reference,args):return corpus_line16.oracle(reference,args) if reference=="16.14" else base_oracle(reference,args)
from generate import generate
from models16 import declare,header,neutral

def generate16():
    for spec in SPECS:
        if oracle(spec['ref'],spec['example'][0])!=spec['example'][1]:raise ValueError('Incorrect example '+spec['ref'])
        cases(spec)
    generate(specs=SPECS,algorithm=body,corpus=cases,reference=oracle,headers={language:header('16',language) for language in LANGUAGES},declare=declare,neutral=neutral,staging_name='staged16')

    for spec in SPECS:
        for language,detail in spec.get('languageWhy',{}).items():
            path=ROOT/'ctci6/staged16'/language/('ctci6_'+spec['ref'].replace('.','_')+'.json')
            notes=json.loads(path.read_text());notes['explanation']+=' '+detail
            path.write_text(json.dumps(notes,indent=2)+'\n')

if __name__=='__main__':generate16()
