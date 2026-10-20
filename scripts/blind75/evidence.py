"""Require all 1,125 current cells, rejecting stale source/corpus/harness results."""
import hashlib,json
from generate import ROOT,LANGS

def sha(text):return hashlib.sha256(text.encode()).hexdigest().upper()

def main():
    catalog=json.loads((ROOT/'blind75/catalog.json').read_text());all_rows={}
    manifest=json.loads((ROOT/'.epi-runs/blind75-harnesses.json').read_text())
    for path,digest in manifest['sourceFiles'].items():assert sha((ROOT/path).read_text())==digest, 'Rebuild audit and run describe: '+path
    harnesses={(r['problem'],r['language']):r['harnessSha256'] for r in manifest['harnesses']}
    paths=sorted((ROOT/'.epi-runs').glob('blind75-audit-*.json'),key=lambda p:p.stat().st_mtime)
    for path in paths:
        for row in json.loads(path.read_text()):all_rows.setdefault((row['problem'],row['language'],row['variant']),[]).append(row)
    accepted=[];missing=[]
    for d in catalog:
        corpus=sha((ROOT/'blind75/cases'/f'{d["id"]}.json').read_text())
        for lang in LANGS:
            bridge=harnesses[d['id'],lang]
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
    adversaries=[]
    for d in catalog:
        if d['mode'] not in ('strings_codec','tree_codec'):continue
        corpus=sha((ROOT/'blind75/cases'/f'{d["id"]}.json').read_text())
        for lang in LANGS:
            code=(ROOT/'scripts/blind75/fixtures/adversarial'/lang/d['id']/d['starters'][lang]['filename']).read_text()
            matches=[r for r in all_rows.get((d['id'],lang,'adversarial'),[]) if r.get('codeSha256')==sha(code) and r.get('corpusSha256')==corpus and r.get('harnessSha256')==harnesses[d['id'],lang]]
            assert matches and matches[-1]['success'] and matches[-1]['result']['Status']=='Wrong answer',(d['id'],lang,'static-memory adversary')
            adversaries.append(matches[-1])
    assert len(adversaries)==10
    summary=dict(catalogSha256=sha((ROOT/'blind75/catalog.json').read_text()),problemCount=75,languageCount=5,currentExecutions=1125,
      variants={v:sum(r['variant']==v for r in accepted) for v in ['starter','correct','incorrect']},
      languages={l:sum(r['language']==l for r in accepted) for l in LANGS},
      staticMemoryAdversaries=len(adversaries),corpusCases=sum(d['testCount'] for d in catalog),positiveCaseEvaluations=sum(d['testCount'] for d in catalog)*5)
    (ROOT/'.epi-runs/blind75-matrix-final.json').write_text(json.dumps(dict(summary=summary,executions=accepted,adversaries=adversaries),indent=2)+'\n')
    print('PASS',json.dumps(summary))
if __name__=='__main__':main()
