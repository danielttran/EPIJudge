"""Generate a frozen reviewed batch through existing local formatting paths."""
from algorithms17 import body
from chapter17 import SPECS
from core import LANGUAGES
from corpus17 import cases,oracle
from generate import generate
from models17 import declare,header,neutral

def generate17():
    for spec in SPECS:
        if oracle(spec['ref'],spec['example'][0])!=spec['example'][1]:raise ValueError('Incorrect example '+spec['ref'])
        cases(spec)
    generate(specs=SPECS,algorithm=body,corpus=cases,reference=oracle,headers={language:header('17',language) for language in LANGUAGES},declare=declare,neutral=neutral,staging_name='staged17')

if __name__=='__main__':generate17()
