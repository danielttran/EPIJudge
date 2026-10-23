"""Generate independently authored native-worker contracts and language notes."""
import json
from algorithms15 import body
from chapter15 import SPECS
from core import ROOT,LANGUAGES
from corpus15 import cases,oracle
from generate import generate
from models15 import declare,header,neutral

def generate15():
 rows=[]
 for spec in SPECS:
  generate(specs=[spec],algorithm=body,corpus=cases,reference=oracle,declare=declare,headers={language:header(spec['ref'],language) for language in LANGUAGES},neutral=neutral,staging_name='staged15')
  rows.extend(json.loads((ROOT/'ctci6/staged15/catalog.json').read_text()))
 (ROOT/'ctci6/staged15/catalog.json').write_text(json.dumps(rows,indent=2)+'\n')
 for spec in SPECS:
  for language,detail in spec['languageWhy'].items():
   p=ROOT/'ctci6/staged15'/language/('ctci6_'+spec['ref'].replace('.','_')+'.json');notes=json.loads(p.read_text());notes['explanation']+=' '+detail;p.write_text(json.dumps(notes,indent=2)+'\n')
if __name__=='__main__':generate15()
