"""Isolated real-HTTP/browser checks. Starts only temporary local profiles.

All five intentional timeouts run unless --no-timeouts is explicitly requested;
a skipped timeout run is reported as such and is not final acceptance evidence.
"""
import argparse,json,os,socket,subprocess,tempfile,time,http.client,threading
from pathlib import Path
from urllib.parse import urlsplit
from contextlib import ExitStack

ROOT=Path(__file__).resolve().parents[1]
LANGUAGES=['csharp','javascript','python','cpp','java']
HEADERS={'X-EpiJudge-Client':'local-editor','Content-Type':'application/json'}
CHECKS=[]
def create_run_directory(root):
    artifact_root=root/'.epi-runs'
    artifact_root.mkdir(parents=True,exist_ok=True)
    return Path(tempfile.mkdtemp(prefix='blind75-http-',dir=artifact_root))

def check(ok,label):
    if not ok:raise AssertionError(label)
    CHECKS.append(label);print('PASS '+label,flush=True)
def request(base,path,method='GET',body=None,headers=HEADERS,raw=False):
    url=urlsplit(base);connection=http.client.HTTPConnection(url.hostname,url.port,timeout=150)
    try:
        data=body if raw else json.dumps(body) if body is not None else None
        connection.request(method,path,data,headers);response=connection.getresponse();payload=response.read();status=response.status;meta=dict(response.getheaders())
        try:payload=json.loads(payload)
        except (json.JSONDecodeError,UnicodeDecodeError):pass
        return status,payload,meta
    finally:connection.close()
def api(base,path,method='GET',body=None):
    status,payload,_=request(base,path,method,body);check(status==200,f'{method} {path} returns 200');return payload
class Server:
    def __init__(self,dll,directory):
        with socket.socket() as listener:listener.bind(('127.0.0.1',0));port=listener.getsockname()[1]
        self.base=f'http://127.0.0.1:{port}';self.log=open(directory/'server.log','w');env=os.environ.copy();env.update(ASPNETCORE_ENVIRONMENT='Development',Frontend__Enabled='false',Practice__DataDirectory=str(directory/'profile'))
        self.process=subprocess.Popen(['dotnet',str(dll),'--urls',self.base,'--contentRoot',str(ROOT/'EpiJudge.Web')],cwd=ROOT,env=env,stdout=self.log,stderr=subprocess.STDOUT)
        for _ in range(100):
            if self.process.poll() is not None:raise RuntimeError('Server exited: '+str(directory/'server.log'))
            try:
                if request(self.base,'/api/health')[0]==200:return
            except (ConnectionError,OSError):pass
            time.sleep(.1)
        raise RuntimeError('Server did not become ready: '+str(directory/'server.log'))
    def close(self):
        if self.process.poll() is None:
            try:request(self.base,'/api/internal/shutdown','POST')
            except (ConnectionError,OSError):pass
            try:self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:self.process.kill();self.process.wait()
        self.log.close()
def fixture(s,lang,variant='correct'):
    return (ROOT/'scripts/blind75/fixtures'/variant/lang/s['id']/s['starters'][lang]['filename']).read_text()
def judge(base,s,lang,code,mode='submit'):
    return request(base,'/api/submissions','POST',dict(problemId=s['id'],language=lang,code=code,mode=mode))
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--dll',type=Path,required=True);parser.add_argument('--browser',action='store_true');parser.add_argument('--no-timeouts',action='store_true');args=parser.parse_args()
    catalog=json.loads((ROOT/'blind75/catalog.json').read_text());by_id={p['id']:p for p in catalog};number=by_id['blind75_number_of_1_bits'];two=by_id['blind75_two_sum']
    run_dir=create_run_directory(ROOT)
    with ExitStack() as stack:
        server=Server(args.dll.resolve(),run_dir);stack.callback(server.close);base=server.base
        problems=api(base,'/api/problems');check(len(problems)==293,'API retains 218 EPI plus 75 Blind entries');check(sum(p['collection']=='epi' for p in problems)==218,'EPI identity count remains 218')
        check([p['title'] for p in problems if p['collection']=='blind75']==(ROOT/'blind75/source-order.txt').read_text().splitlines(),'HTTP catalog has exact Crackr ordering')
        check(all(set(p['starters'])==set(LANGUAGES) for p in problems),'all 293 API entries expose five starters');check(all('invocation' not in p and 'harnessConfigs' not in p for p in problems),'API omits internal grading configuration')
        for lang in LANGUAGES:check(len(api(base,'/api/problems?lang='+lang))==293,lang+' catalog query remains supported')
        for asset in json.loads((ROOT/'blind75/diagrams.json').read_text()):
            status,data,headers=request(base,asset['path']);check(status==200 and data==(ROOT/'EpiJudge.Web/wwwroot'/asset['path'].lstrip('/')).read_bytes(),asset['id']+' local SVG served byte-for-byte')
            check(headers.get('Content-Type','').startswith('image/svg+xml'),'SVG has correct media type')
        check(request(base,'/api/not-a-real-endpoint')[0]==404,'unknown API routes return 404')
        valid=dict(problemId=two['id'],language='javascript',mode='run',code=fixture(two,'javascript'))
        for field,value in [('problemId','unknown'),('problemId',None),('language','ruby'),('mode','other'),('code',''),('code','x'*40001)]:
            body=dict(valid);body[field]=value;check(request(base,'/api/submissions','POST',body)[0]==400,'invalid submission '+field+' rejected')
        check(request(base,'/api/submissions','POST',valid,headers={'Content-Type':'application/json'})[0]==403,'submission write requires same-app header')
        check(request(base,'/api/submissions','POST','{broken json',raw=True)[0]==400,'malformed request JSON rejected')
        for backup in [dict(version=999,drafts=[],attempts=[],solvedIds=[]),dict(version=1,drafts=None,attempts=[],solvedIds=[])]:check(request(base,'/api/practice/import','POST',backup)[0]==400,'invalid backup rejected')
        for lang in LANGUAGES:
            for id_ in ['two_sum',two['id']]:api(base,f'/api/practice/drafts/{id_}/{lang}','PUT',dict(code='draft '+id_+' '+lang,revision=0))
        check(request(base,f'/api/practice/drafts/{two["id"]}/python','PUT',dict(code='stale',revision=0))[0]==409,'stale Blind draft revision rejected')
        status,accepted,_=judge(base,two,'javascript',fixture(two,'javascript'));check(status==200 and accepted['status']=='Accepted','Blind 75 actual algorithm accepted through HTTP')
        history=api(base,'/api/practice/history/'+accepted['id']);check(history['code']==fixture(two,'javascript'),'history stores exact source');check(not history['result']['cases'],'accepted Submit stores no hidden case contents')
        status,visible,_=judge(base,two,'javascript',fixture(two,'javascript'),'run');check(status==200 and visible['status']=='Accepted' and len(visible['cases'])==3 and all(not c['hidden'] for c in visible['cases']),'Run shows exactly three visible examples')
        status,wrong,_=judge(base,two,'javascript',fixture(two,'javascript','incorrect'));check(status==200 and wrong['status']=='Wrong answer' and all(c['hidden'] and c['input'] is None and c['actual'] is None and c['expected'] is None for c in wrong['cases']),'failed Submit hides all case contents')
        for lang in LANGUAGES:
            starter=number['starters'][lang]['starterCode'];bad=starter+'\ninvalid syntax !!!'
            status,result,_=judge(base,number,lang,bad,'run');check(status==200 and result['status']==('Runtime error' if lang in ('python','javascript') else 'Compilation error'),lang+' syntax error reported')
            throws={'csharp':'throw new Exception("fixture");','javascript':'throw new Error("fixture");','python':'raise RuntimeError("fixture")','cpp':'throw std::runtime_error("fixture");','java':'throw new RuntimeException("fixture");'}[lang]
            source=starter.replace('return 0' if lang=='python' else 'return 0;',throws)
            if lang=='cpp':source='#include <stdexcept>\n'+source
            status,result,_=judge(base,number,lang,source,'run');check(status==200 and result['status']=='Runtime error',lang+' runtime error reported')
        if not args.no_timeouts:
            for lang in LANGUAGES:
                source=number['starters'][lang]['starterCode'].replace('return 0' if lang=='python' else 'return 0;','while True: pass' if lang=='python' else 'while (true) {}')
                response=[]
                worker=threading.Thread(target=lambda:response.append(judge(base,number,lang,source,'run')));worker.start()
                running=False
                for _ in range(150):
                    status,history,_=request(base,'/api/practice/history?problemId='+number['id'])
                    if status==200 and any(h['status']=='Running' for h in history):running=True;break
                    time.sleep(.1)
                check(running,lang+' timeout source durably recorded while running')
                check(judge(base,two,'javascript',fixture(two,'javascript'))[0]==429,lang+' busy runner returns 429')
                worker.join(140);check(not worker.is_alive() and response and response[0][0]==200 and response[0][1]['status']=='Time limit exceeded',lang+' actual timeout enforced')
                check(judge(base,two,'javascript',fixture(two,'javascript'))[1]['status']=='Accepted',lang+' runner recovers after timeout')
        else:print('SKIPPED five intentional timeout checks; not final acceptance evidence',flush=True)
        if args.browser:subprocess.run(['node',str(ROOT/'scripts/verify_blind75_browser.cjs'),base],check=True,cwd=ROOT)
        backup=api(base,'/api/practice/export');destination=run_dir/'restored';destination.mkdir();restored=Server(args.dll.resolve(),destination);stack.callback(restored.close)
        api(restored.base,'/api/practice/import','POST',backup);api(restored.base,'/api/practice/import','POST',backup);state=api(restored.base,'/api/practice')
        check(len(state['drafts'])==len(backup['drafts']),'backup restores all EPI/Blind/language drafts without duplication')
        restored_history=api(restored.base,'/api/practice/history/'+accepted['id']);check(restored_history['code']==fixture(two,'javascript'),'backup restores exact Blind historical source')
        check(len(api(restored.base,'/api/practice/history?problemId='+two['id']))==sum(a['problemId']==two['id'] for a in backup['attempts']),'repeated backup import has no duplicate Blind history')
        (ROOT/'.epi-runs/blind75-http.json').write_text(json.dumps(dict(checks=CHECKS,timeoutsSkipped=args.no_timeouts,browser=args.browser,logDirectory=str(run_dir)),indent=2)+'\n')
        print(f'PASS all {len(CHECKS)} HTTP checks; browser={args.browser}; timeoutsSkipped={args.no_timeouts}',flush=True)
if __name__=='__main__':main()
