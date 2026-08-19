from pathlib import Path
import json, re, urllib.request, sys
ROOT=Path('/Users/knowurknot/inversion-labs-skills'); UP=Path('/Users/knowurknot/.agents/skills'); OUT=ROOT/'evals/local-qwen'; OUT.mkdir(parents=True,exist_ok=True)
CASES={
 'interface': {
  'files':[UP/'taste/SKILL.md',UP/'design-taste-frontend/SKILL.md',UP/'impeccable/SKILL.md'],
  'overlay':ROOT/'skills/inversion-interface-craft/SKILL.md',
  'scenario':ROOT/'evals/baseline/prompt-interface.txt',
  'checks':{
   'impeccable_owns':r'(primary owner|primary skill).{0,100}impeccable|impeccable.{0,100}(primary owner|primary skill)',
   'dashboard_excludes_marketing_taste':r'(dashboard|operator).{0,500}(design-taste-frontend).{0,180}(none|excluded|do not load|not load|no role)|design-taste-frontend.{0,180}(none|excluded|do not load|not load|no role).{0,500}(dashboard|operator)',
   'precedence':r'(brief|product truth).{0,500}(safety|accessibility).{0,500}(contract|platform|interaction).{0,600}taste',
   'bounded_stop':r'(batch|batched).{0,180}(confirm|confirmation).{0,180}(stop|STOP)',
   'evidence':r'screenshot.{0,500}(keyboard|focus|contrast|state|responsive)',
  }
 },
 'motion': {
  'files':[UP/'taste/SKILL.md',UP/'hyperframes/SKILL.md',UP/'hyperframes-core/SKILL.md',UP/'hyperframes-creative/SKILL.md',UP/'impeccable/SKILL.md'],
  'overlay':ROOT/'skills/inversion-motion-craft/SKILL.md',
  'scenario':ROOT/'evals/baseline/prompt-motion.txt',
  'checks':{
   'root_hyperframes_owner':r'primary owner.{0,80}`?hyperframes`?(?!-)|`?hyperframes`?.{0,80}primary owner',
   'impeccable_conditional':r'impeccable.{0,250}(only if|only when|if actual|when actual|when any interface|confined to|conditional)',
   'technical_contract_wins':r'hyperframes technical contract|technical contract.{0,180}(win|preced|override)|seek-safe.{0,180}(change the idea|contract)',
   'motion_purpose_ledger':r'motion purpose ledger',
   'ledger_has_decision_schema':r'viewer-visible change.{0,180}(keep|delete)|keep/delete',
   'render_evidence':r'hyperframes (check|render).{0,400}(frame|clip|boundary|sync|evidence|verify)',
  }
 }
}
def call(prompt):
 body=json.dumps({'model':'qwen3.5-defiant-fable:latest','messages':[{'role':'user','content':prompt}],'stream':False,'think':False,'options':{'temperature':0,'num_predict':1800,'num_ctx':65536}}).encode()
 req=urllib.request.Request('http://127.0.0.1:11434/api/chat',data=body,headers={'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=300) as r:return json.load(r)['message']['content']
results={}
selected=set(sys.argv[1:]) if len(sys.argv)>1 else set(CASES)
for name,c in CASES.items():
 if name not in selected: continue
 upstream='\n\n'.join(f'### UPSTREAM {p.parent.name}\n{p.read_text()}' for p in c['files'])
 prompt=f'''Treat these upstream skill texts as authoritative mechanics.\n\n{upstream}\n\nINVERSION LABS OVERLAY (authoritative for ownership/conflict/finish)\n{c['overlay'].read_text()}\n\nSCENARIO\n{c['scenario'].read_text()}\n\nAnswer operationally and obey every required handoff/output contract in the overlay.'''
 text=call(prompt); (OUT/f'{name}-final.txt').write_text(text+'\n')
 checks={k:bool(re.search(rx,text,re.I|re.S)) for k,rx in c['checks'].items()}; results[name]=checks
 print(name, f'{sum(checks.values())}/{len(checks)}', checks, flush=True)
(OUT/'final-results.json').write_text(json.dumps(results,indent=2)+'\n')
