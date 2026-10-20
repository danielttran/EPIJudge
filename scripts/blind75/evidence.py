"""Require all 1,125 current cells, rejecting stale source/corpus/harness results."""
import hashlib,json
from generate import ROOT,LANGS

def sha(text):return hashlib.sha256(text.encode()).hexdigest().upper()
def harness(definition,language):
    filename=dict(csharp='Harness.cs',java='Harness.java',cpp='harness.cpp',python='harness.py',javascript='harness.js')[language]
    source=(ROOT/'blind75/runtime'/filename).read_text();config=definition['harnessConfigs'][language]
    if language in ('csharp','java'):return source.replace('// CONFIGURATION',config)
    if language=='cpp':return source.replace('// EXECUTE',config)
    return config+source

def main():
    catalog=json.loads((ROOT/'blind75/catalog.json').read_text());all_rows={}
    paths=sorted((ROOT/'.epi-runs').glob('blind75-audit-all-*.json'),key=lambda p:p.stat().st_mtime)
    for path in paths:
        for row in json.loads(path.read_text()):all_rows.setdefault((row['problem'],row['language'],row['variant']),[]).append(row)
    accepted=[];missing=[]
    for d in catalog:
        corpus=sha((ROOT/'blind75/cases'/f'{d["id"]}.json').read_text())
        for lang in LANGS:
            bridge=sha(harness(d,lang))
            for variant in ['starter','correct','incorrect']:
                code=d['starters'][lang]['starterCode'] if variant=='starter' else (ROOT/'scripts/blind75/fixtures'/variant/lang/d['id']/d['starters'][lang]['filename']).read_text()
                matches=[r for r in all_rows.get((d['id'],lang,variant),[]) if r.get('codeSha256')==sha(code) and r.get('corpusSha256')==corpus and r.get('harnessSha256')==bridge]
                if not matches or not matches[-1]['success']:missing.append((d['id'],lang,variant));continue
                row=matches[-1];assert row['result']['Total']==d['testCount'],(d['id'],lang,'stale count')
                if variant=='correct':assert row['result']['Status']=='Accepted' and row['result']['Passed']==d['testCount']
                if variant=='incorrect':assert row['result']['Status']=='Wrong answer' and row['result']['Passed']<d['testCount']
                accepted.append(row)
    if missing:raise AssertionError('Missing, stale, or failed current executions: '+repr(missing))
    assert len(accepted)==1125
    summary=dict(catalogSha256=sha((ROOT/'blind75/catalog.json').read_text()),problemCount=75,languageCount=5,currentExecutions=1125,
      variants={v:sum(r['variant']==v for r in accepted) for v in ['starter','correct','incorrect']},
      languages={l:sum(r['language']==l for r in accepted) for l in LANGS},
      corpusCases=sum(d['testCount'] for d in catalog),positiveCaseEvaluations=sum(d['testCount'] for d in catalog)*5)
    (ROOT/'.epi-runs/blind75-matrix-final.json').write_text(json.dumps(dict(summary=summary,executions=accepted),indent=2)+'\n')
    print('PASS',json.dumps(summary))
if __name__=='__main__':main()
