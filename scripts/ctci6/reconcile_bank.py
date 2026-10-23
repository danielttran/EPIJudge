"""Join real whole-bank execution receipts to final per-pair source fingerprints.

This consumes local raw execution artifacts. Inventory or filled prose fields alone
never grant execution credit. Publication still requires eligible inventory closure.
"""
import argparse
from collections import defaultdict
import hashlib,json
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
LANGUAGES=('csharp','javascript','python','cpp','java')
FIELDS=('codeSha256','composedCodeSha256','notesSha256','corpusSha256','harnessSha256')
def read(path):return json.loads((ROOT/path).read_text())
def sha(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
def key(row):return row['problemId'],row['language']
def expected_key(value):
    # Displayed double results may spell 5.0 as 5. Preserve all other JSON
    # types, especially booleans versus numbers, and keep arguments exact.
    if isinstance(value,bool):return ('boolean',value)
    if isinstance(value,(int,float)):
        numerator,denominator=Decimal(str(value)).as_integer_ratio();return ('number',numerator,denominator)
    if value is None:return ('null',)
    if isinstance(value,str):return ('string',value)
    if isinstance(value,list):return ('array',[expected_key(v)for v in value])
    return ('object',[(k,expected_key(v))for k,v in sorted(value.items())])
def case_key(case):return json.dumps([case.get('arguments',case.get('Arguments')),expected_key(case.get('expected',case.get('Expected')))],sort_keys=True,separators=(',',':'))
def main(tag):
    receipts={};provenance={};records=[]
    fingerprints={role:{key(r):r for r in read('.epi-runs/solutions-fingerprints-'+('correct'if role=='solution'else'starters')+'.json')['fingerprints']}for role in ('solution','starter')}
    current=fingerprints['solution'];original={k for k,v in current.items()if v['collection']!='ctci6'};ctci=set(current)-original
    def merge(path,destination):
        report=read(path);receipts[path]=sha(path)
        for row in report['executions']:destination[key(row)]=(row,path)
    for role in ('solution','starter'):
        merged={};label='correct'if role=='solution'else'starter'
        for language in LANGUAGES:merge(f'.epi-runs/solutions-audit-callable-{label}-{language}-clarity-final.json',merged)
        merge('.epi-runs/solutions-audit-wholebank-overlap-'+('correct'if role=='solution'else'starters')+'.json',merged)
        for language in LANGUAGES:merge(f'.epi-runs/solutions-audit-{tag}-{language}-'+('correct'if role=='solution'else'starters')+'.json',merged)
        for language in ("python","javascript","cpp"):
            merge(f'.epi-runs/solutions-audit-ctci6-tail131-{language}-'+('correct'if role=='solution'else'starters')+'.json',merged)
        assert set(merged)==set(current),'Missing/extraneous corpus execution pairs'
        for pair,(row,path)in merged.items():
            assert row['success'] is True,(pair,'failed receipt')
            assert row['role']==role and row['codeFormat']=='callable-v1',(pair,'wrong execution boundary')
            for field in FIELDS:assert row[field]==fingerprints[role][pair][field],(pair,field,'stale receipt')
            if role=='solution':assert row['result']['Status']=='Accepted'and row['result']['Passed']==row['result']['Total'],(pair,'incomplete corpus')
            else:assert row['result']['Status']!='Accepted',(pair,'accepted starter')
            records.append(dict(fingerprints[role][pair],receipt=path,resultStatus=row['result']['Status'],passedCases=row['result']['Passed'],totalCases=row['result']['Total'],success=True))
    # The original bank has separate executed examples and boundary fixtures.
    examples={};boundaries={}
    for language in LANGUAGES:
        p='.epi-runs/solutions-callable-walkthroughs-'+('whole-bank-csharp-current'if language=='csharp'else language)+'.json';merge(p,examples)
        if language!='csharp':merge(f'.epi-runs/ctci6-overlap130/solutions-callable-walkthroughs-{language}.json',examples)
        suffix={'csharp':'csharp-before-fixture-corrections','cpp':'cpp-before-fixture-corrections','python':'python-before-wrapper-correction'}.get(language,language)
        merge('.epi-runs/solutions-callable-boundaries-'+suffix+'.json',boundaries)
        if language in ('csharp','cpp','python'):merge('.epi-runs/solutions-callable-boundaries-whole-bank-current-'+language+'.json',boundaries)
    assert set(examples)==original and set(boundaries)==original,'Incomplete original example/boundary executions'
    current_boundaries=defaultdict(set)
    for p in sorted((ROOT/'scripts/solutions').glob('boundaries-*.json')):
        for case in json.loads(p.read_text()):current_boundaries[case['problemId']].add(case_key(case))
    supplemental=[]
    for label,merged in [('walkthrough',examples),('boundary',boundaries)]:
        for pair,(row,path)in merged.items():
            assert row['success']and row['result']['Status']=='Accepted',(label,pair,'failed')
            for field in FIELDS[:2]:assert row[field]==current[pair][field],(label,pair,field,'stale')
            pid,language=pair;notes=read('solutions/notes/'+(''if language=='csharp'else language+'/')+pid+'.json')
            expected={case_key(notes['walkthroughCase'])}if label=='walkthrough'else current_boundaries[pid]
            observed={case_key(case)for case in row['cases']}
            assert observed==expected,(label,pair,'fixtures changed')
            supplemental.append(dict(problemId=pid,language=language,kind=label,cases=row['result']['Total'],receipt=path,success=True))
    # Each CtCI worked example is a row in the actually executed current corpus;
    # property graders may accept multiple correct outputs, as the problem states.
    for pair in ctci:
        pid,language=pair;notes=read('solutions/notes/'+(''if language=='csharp'else language+'/')+pid+'.json');corpus=read('ctci6/cases/'+pid+'.json')
        assert case_key(notes['walkthroughCase'])in{case_key(c)for c in corpus},(pair,'example absent from executed corpus')
    inv=read('ctci6/inventory.json');correct=[r for r in records if r['role']=='solution'];starters=[r for r in records if r['role']=='starter']
    source_paths=set(read('.epi-runs/solutions-fingerprints-correct.json')['sourceHashes'])
    source_paths.update(['solutions/catalog.json','solutions/coverage.json','scripts/ctci6/reconcile_bank.py','scripts/ctci6/test_reconcile_bank.py','scripts/SolutionsAudit/Program.cs'])
    for entry in read('solutions/coverage.json')['entries']:
        source_paths.update([entry['codePath'],entry['notesPath']])
        source_paths.add(entry['collection']+'/cases/'+entry['problemId']+'.json' if entry['collection'] in ('blind75','interviewcake','ctci6') else 'test_data/'+entry['problemId']+'.tsv')
    source_hashes={p:sha(p)for p in sorted(source_paths)}
    result=dict(schemaVersion=1,status='passed-current-registered-bank',publicationReady=False,scope=dict(registeredQuestions=len(current)//5,executedSolutionPairs=len(correct),rejectedStarterPairs=len(starters),originalSolutionPairs=len(original),ctciSolutionPairs=len(ctci),solutionCaseExecutions=sum(r['totalCases']for r in correct),starterCaseObservations=sum(r['totalCases']for r in starters),originalSeparateWalkthroughPairs=len(examples),originalSeparateBoundaryPairs=len(boundaries),ctciWalkthroughPairsIncludedInExecutedCorpus=len(ctci)),inventory=dict(identified=inv['scope']['identifiedNumberedReferences'],pendingCodingReferences=[q['ref']for q in inv['questions']if q['classification']=='coding-candidate']),receiptHashes=receipts,sourceHashes=source_hashes,sharedDispatchReview='Compared original clarity acceptance dispatch/envelope source at 3c1c5014543bd8b2d9ddf2972794474951cdd9a8: the callable preparation body is unchanged after extraction into PrepareCallable; added collection-size checks and CtCI dispatch do not change original prepared code. Current per-pair code, composed source, notes, corpus and harness hashes must all match each reused original corpus receipt. Changed overlap composition/notes and corrected original fixtures have fresh executions.',claimLimit='Actual current registered-bank application-callable execution only. It does not implement eight pending CtCI contracts, grant semantic review from structural presence, or establish publication/CI completion.',executions=records,supplementalExecutions=supplemental)
    out=ROOT/'ctci6/whole-bank-validation.json';out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k not in ('receiptHashes','sourceHashes','executions','supplementalExecutions')},indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--tag',default='ctci6-final131');main(p.parse_args().tag)
