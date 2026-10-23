"""Preflight all graph fixtures before generating the chapter snapshot."""
from algorithms04 import body
from chapter04 import SPECS
from core import LANGUAGES
from corpus04 import cases,oracle
from generate import generate
from models04 import declare,header,neutral

def generate04():
    for spec in SPECS:
        if oracle(spec['ref'],spec['example'][0])!=spec['example'][1]:raise ValueError('Incorrect example '+spec['ref'])
        cases(spec)
    generate(specs=SPECS,algorithm=body,corpus=cases,reference=oracle,headers={language:header('4',language) for language in LANGUAGES},declare=declare,neutral=neutral,staging_name='staged04')

if __name__=='__main__':generate04()
