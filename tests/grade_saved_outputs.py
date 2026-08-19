from pathlib import Path
import json, re, sys
ROOT=Path('/Users/knowurknot/inversion-labs-skills')
OUT=ROOT/'evals/local-qwen'
CASES={
 'interface':{
  'checks':{
   'impeccable_owns':r'(primary owner|primary skill|primary:).{0,100}`?impeccable`?|`?impeccable`?.{0,100}(primary owner|primary skill)',
   'dashboard_excludes_marketing_taste':r'(dashboard|operator).{0,1400}(design-taste-frontend).{0,240}(none|excluded|do not load|not loaded|not applied|no role)|design-taste-frontend.{0,240}(none|excluded|do not load|not loaded|not applied|no role).{0,1400}(dashboard|operator)',
   'precedence':r'(brief|product truth).{0,500}(safety|accessibility).{0,500}(contract|platform|interaction).{0,700}taste',
   'bounded_stop':r'(batch|batched).{0,180}(confirm|confirmation).{0,180}(stop|STOP)',
   'evidence':r'screenshot.{0,700}(keyboard|focus|contrast|state|responsive)',
  }
 },
 'motion':{
  'checks':{
   'root_hyperframes_owner':r'primary owner\s*:\s*`?hyperframes`?(?!-)',
   'impeccable_conditional':r'impeccable.{0,300}(only if|only when|if actual|when actual|when any interface|when actual interface|constrained to|confined to)',
   'technical_contract_wins':r'hyperframes technical contract|technical contract.{0,220}(win|preced|override)|seek-safe.{0,220}(change the idea|contract)',
   'motion_purpose_ledger':r'motion purpose ledger',
   'ledger_has_decision_schema':r'viewer-visible change.{0,220}(keep/delete|keep|delete)',
   'render_evidence':r'hyperframes (check|render).{0,500}(frame|clip|boundary|sync|evidence|verify|determin)',
   'claim_integrity':r'(no claims|claimless|supplied|verified).{0,260}(claim|metric|truth|data)|claim integrity',
  }
 }
}
all_results={}; failed=False
for name,cfg in CASES.items():
 p=OUT/f'{name}-final.txt'
 if not p.exists():
  print(f'MISSING {p}'); failed=True; continue
 text=p.read_text()
 checks={k:bool(re.search(rx,text,re.I|re.S)) for k,rx in cfg['checks'].items()}
 all_results[name]={'passed':sum(checks.values()),'total':len(checks),'checks':checks}
 print(f'{name}: {sum(checks.values())}/{len(checks)} {checks}')
 failed |= not all(checks.values())
(OUT/'final-results.json').write_text(json.dumps(all_results,indent=2)+'\n')
sys.exit(1 if failed else 0)
