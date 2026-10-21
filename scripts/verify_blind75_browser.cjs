// Real Chromium, Monaco, HTTP persistence and locally served assets; no mocks.
const fs=require('node:fs');
const path=require('node:path');
const assert=require('node:assert/strict');
const {chromium}=require('../epijudge.client/node_modules/playwright-core');
const base=process.argv[2];
const root=path.resolve(__dirname,'..');
fs.mkdirSync(path.join(root,'.epi-runs'),{recursive:true});
const messages=[];
function pass(label){messages.push(label);console.log('PASS browser '+label);}
async function until(predicate,label){const end=Date.now()+20000;while(Date.now()<end){if(await predicate())return;await new Promise(r=>setTimeout(r,100));}throw Error('Timed out: '+label);}
(async()=>{
 const browser=await chromium.launch({headless:true,...(process.env.CHROMIUM_PATH?{executablePath:process.env.CHROMIUM_PATH}:{}),args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1440,height:1000},acceptDownloads:true});
 const page=await context.newPage();const errors=[],external=[];
 page.on('pageerror',e=>errors.push(String(e)));
 await context.route('**/*',route=>{const url=new URL(route.request().url());if(['http:','https:'].includes(url.protocol)&&url.origin!==new URL(base).origin){external.push(url.href);return route.abort();}return route.continue();});
 try{
  await page.goto(base,{waitUntil:'networkidle'});
  await page.getByRole('combobox',{name:'Select programming language'}).waitFor();
  const open=async()=>{await page.getByRole('button',{name:'Toggle problem list'}).click();};
  const filter=page.getByRole('combobox',{name:'Filter by topic or study plan'});
  await open();await filter.selectOption('collection:blind75');
  assert.equal(await page.locator('nav[aria-label="Problems"] button').count(),75);
  await page.getByRole('textbox',{name:'Search problems'}).fill('not-an-existing-problem');
  assert.equal(await page.locator('nav[aria-label="Problems"] button').count(),0);
  await page.getByRole('textbox',{name:'Search problems'}).fill('');
  await filter.selectOption('collection:epi');assert.equal(await page.locator('nav[aria-label="Problems"] button').count(),218);
  await filter.selectOption('collection:blind75');await page.getByRole('button',{name:/^B01\. Two Sum/}).click();
  assert.match(await page.locator('h1').textContent(),/B01\. Two Sum/);
  await page.getByRole('button',{name:'Next problem',exact:true}).click();await until(async()=>/B02/.test(await page.locator('h1').textContent()),'Blind next');
  await page.getByRole('button',{name:'Previous problem',exact:true}).click();await until(async()=>/B01/.test(await page.locator('h1').textContent()),'Blind previous');
  pass('75/218 collection filters, empty search, and bounded collection navigation');
  const language=page.getByRole('combobox',{name:'Select programming language'});
  const editor=page.locator('.monaco-editor textarea.inputarea');
  async function edit(code){await editor.focus();await page.keyboard.press('Control+A');await page.keyboard.insertText(code);}
  async function saved(id,lang,code){await until(async()=>{const response=await page.request.get(base+'/api/practice');const state=await response.json();return state.drafts.some(d=>d.problemId===id&&d.language===lang&&d.code===code);},'save '+id+'/'+lang);}
  for(const lang of ['csharp','javascript','python','cpp','java']){
   await language.selectOption(lang);const code=(lang==='python'?'#':'//')+' browser draft '+lang;await edit(code);await saved('blind75_two_sum',lang,code);
  }
  await language.selectOption('javascript');
  await until(async()=>((await page.locator('.monaco-editor .view-lines').innerText()).replace(/\s+/g,' ').includes('browser draft javascript')),'language draft restore');
  pass('real Monaco editing and independent drafts in all five languages');
  const correct='function twoSum(nums,target){const seen=new Map();for(let i=0;i<nums.length;i++){if(seen.has(target-nums[i]))return [seen.get(target-nums[i]),i];seen.set(nums[i],i);}return [];} module.exports={twoSum};';
  await edit(correct);await saved('blind75_two_sum','javascript',correct);
  const submissionResponse=page.waitForResponse(r=>r.url()===base+'/api/submissions'&&r.request().method()==='POST');
  const historyResponse=page.waitForResponse(r=>r.url().includes('/api/practice/history?problemId=blind75_two_sum'));
  await page.getByRole('button',{name:'Submit',exact:true}).click();
  assert.equal((await (await submissionResponse).json()).status,'Accepted');
  await historyResponse;
  await until(async()=>{const state=await (await page.request.get(base+'/api/practice')).json();return state.progress.some(p=>p.problemId==='blind75_two_sum'&&p.status==='solved');},'accepted browser submit');
  await page.getByRole('button',{name:'History',exact:true}).click();
  await page.getByRole('button',{name:'View answer',exact:true}).first().click();
  assert.equal(await page.getByLabel('Saved answer code').textContent(),correct);
  await page.getByRole('button',{name:'Restore to editor',exact:true}).click();await saved('blind75_two_sum','javascript',correct);
  pass('Submit, immutable history snapshot and restoring the saved answer');
  await context.route('**/api/practice/drafts/**',route=>route.abort());
  const recovery='// browser recovery survives a failed HTTP save';await edit(recovery);
  await until(async()=>/Save failed/.test(await page.locator('body').textContent()),'recovery warning');
  assert.ok(await page.evaluate(()=>Object.keys(localStorage).some(k=>k.startsWith('epi:pending:'))));
  await context.unroute('**/api/practice/drafts/**');await page.getByRole('button',{name:'Retry save',exact:true}).click();await saved('blind75_two_sum','javascript',recovery);
  await page.reload({waitUntil:'networkidle'});await until(async()=>(await page.locator('.monaco-editor .view-lines').innerText()).replace(/\s+/g,' ').includes('browser recovery survives'),'persisted reload');
  pass('failed-save recovery copy, retry and persistence after reload');
  const catalog=await (await page.request.get(base+'/api/problems')).json();
  const images=catalog.filter(p=>p.collection==='blind75'&&p.diagram).map(p=>p.diagram);assert.equal(images.length,35);
  await page.evaluate(async paths=>{for(const src of paths){const img=new Image();img.src=src;await img.decode();if(!img.naturalWidth)throw Error('Empty image '+src);}},images);
  await open();await filter.selectOption('collection:blind75');await page.getByRole('button',{name:/Rotate Image/}).click();
  await page.locator('figure img').waitFor();assert.ok(await page.locator('figure img').evaluate(img=>img.complete&&img.naturalWidth>0));
  await page.screenshot({path:path.join(root,'.epi-runs/blind75-browser.png'),fullPage:true});
  assert.deepEqual(external,[]);assert.deepEqual(errors,[]);
  pass('all 35 local diagrams decode with every external origin blocked');
  await open();const download=page.waitForEvent('download');await page.getByRole('button',{name:'Export answers',exact:true}).click();
  const file=await download;const backup=JSON.parse(fs.readFileSync(await file.path(),'utf8'));
  assert.equal(backup.version,1);assert.ok(backup.drafts.some(d=>d.problemId==='blind75_two_sum'&&d.language==='javascript'&&d.code===recovery));
  await page.getByLabel('Import answers file').setInputFiles({name:'restored.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(backup))});
  await until(async()=>/Imported answers/.test(await page.locator('dialog').textContent()),'browser import');
  pass('browser backup export/import preserves Blind 75 drafts and history');
  fs.writeFileSync(path.join(root,'.epi-runs/blind75-browser.json'),JSON.stringify({checks:messages,externalRequests:external,pageErrors:errors},null,2));
 }catch(error){await page.screenshot({path:path.join(root,'.epi-runs/blind75-browser-failure.png'),fullPage:true});fs.writeFileSync(path.join(root,'.epi-runs/blind75-browser-failure.txt'),await page.locator('body').innerText());throw error;}finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1);});
