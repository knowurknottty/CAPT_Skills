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
   'dashboard_excludes_marketing_taste':r'(dashboard|operator).{0,500}(design-taste-frontend).{0,180}(none|excluded|do not load|not load|no role|zero authority|does not apply|no .*rules apply)|(do not load|not load|zero authority).{0,100}design-taste-frontend.{0,500}(dashboard|operator)?|design-taste-frontend.{0,180}(none|excluded|do not load|not load|no role|zero authority|does not apply|no .*rules apply).{0,500}(dashboard|operator)',
   'precedence':r'precedence[^:]{0,40}:.{0,120}brief/product truth.{0,120}safety/accessibility/legal.{0,120}interaction/platform contract.{0,160}taste',
   'bounded_stop':r'qa:.{0,100}resolved shipped variants.{0,100}batch-fix.{0,100}confirm once.{0,100}stop',
   'evidence':r'(screenshot|render).{0,500}(keyboard|focus|contrast|state|responsive)',
   'shipped_scope_only':r'shipped.{0,180}(device|theme|mode|variant)|verify what actually ships|only.{0,100}shipped|evidence scope',
   'unknown_scope_preserved':r'evidence scope.{0,80}unknown|device(?: classes)?\s*[=:].{0,30}unknown.{0,120}themes?\s*[=:].{0,30}unknown.{0,120}locales?\s*[=:].{0,30}unknown|unknown.{0,120}device.{0,120}theme.{0,120}locale',
   'pending_scope':r'finish evidence:\s*pending scope.{0,160}resolve evidence scope',
   'constraint_integrity':r'(constraint integrity|no product claims|no .*kpis?|supplied|verified).{0,300}(claim|kpi|threshold|target|benchmark|quantitative|proposed|illustrative)|(?:proposed|illustrative).{0,160}(goal|target|constraint)',
   'assumptions_labeled':r'(audience|preservation).{0,120}(assumed|unknown|proposed|supplied|verified)',
  }
 },
 'motion': {
  'files':[UP/'taste/SKILL.md',UP/'hyperframes/SKILL.md',UP/'hyperframes-core/SKILL.md',UP/'hyperframes-creative/SKILL.md',UP/'impeccable/SKILL.md'],
  'overlay':ROOT/'skills/inversion-motion-craft/SKILL.md',
  'scenario':ROOT/'evals/baseline/prompt-motion.txt',
  'checks':{
   'root_hyperframes_owner':r'primary owner.{0,80}`?hyperframes`?(?!-)|`?hyperframes`?.{0,80}primary owner',
   'impeccable_conditional':r'impeccable.{0,360}(only if|only when|if actual|when actual|when any interface|confined to|conditional|handles any.{0,80}(in-film|product ui)|in-film product ui|depicted (?:product )?ui|only for any depicted|for any depicted)',
   'technical_contract_wins':r'hyperframes technical contract|technical contract.{0,180}(win|preced|override)|seek-safe.{0,180}(change the idea|contract)',
   'motion_purpose_ledger':r'motion purpose ledger',
   'ledger_has_decision_schema':r'job.{0,180}viewer-visible change.{0,180}basis.{0,180}(keep|delete)|basis.{0,120}keep/delete',
   'claim_integrity':r'(claims? integrity|claim status|no invented metrics?|no public metrics?|supplied|verified).{0,300}(claim|metric|product truth|proof|public copy|proposed|evidence|claimless|illustrative)|claimless.{0,160}(copy|creative|frame)',
   'internal_spine_not_public_truth':r'(spine|frame thesis).{0,240}(internal|not.{0,40}(public|claim|on-screen)|proposed creative copy|approved brand line)|proposed creative copy',
   'explicit_claim_status':r'primary owner.{0,80}hyperframes.{0,180}spine/frame thesis.{0,80}internal.{0,180}public copy.{0,120}(supplied|approved|proposed)',
   'audience_assumption_labeled':r'audience assumption.{0,80}(supplied|assumed)',
   'render_scope':r'render(?:/story)? scope.{0,220}duration.{0,180}aspect.{0,180}resolution.{0,180}audio.{0,220}sustained-motion-basis.{0,220}product-state-basis',
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
 prompt=f'''Output exactly the overlay's required handoff slots in at most 600 words. Do not restate upstream checklists or recipes; reference them by skill/playbook and surface only decisions, exceptions, truth status, evidence scope, and proof. Treat these upstream skill texts as authoritative mechanics.\n\n{upstream}\n\nINVERSION LABS OVERLAY (authoritative for ownership/conflict/finish)\n{c['overlay'].read_text()}\n\nSCENARIO\n{c['scenario'].read_text()}\n\nAnswer operationally and obey every required handoff/output contract in the overlay.'''
 text=call(prompt); (OUT/f'{name}-final.txt').write_text(text+'\n')
 checks={k:bool(re.search(rx,text,re.I|re.S)) for k,rx in c['checks'].items()}
 if name=='interface':
  pending=bool(re.search(r'finish evidence:\s*pending scope',text,re.I))
  if pending: checks['evidence']=True
  checks['unknown_not_defaulted']=bool(re.search(r'do not default.{0,80}unknown|unknown.{0,220}(pending scope|do not infer|do not add hypothetical)|pending scope.{0,220}(unknown|resolve evidence scope)',text,re.I|re.S))
  checks['no_operator_marketing_leak']=not bool(re.search(r'\bborrow\b.{0,220}(design-taste|anti-default)|use.{0,80}(?:the )?spirit.{0,160}(design-taste|marketing)',text,re.I|re.S))
  checks['no_invented_variant_coverage']=not bool(re.search(r'both\s+(?:light\s*(?:/|and)\s*dark|dark\s*(?:/|and)\s*light)|shipped\s+(?:mobile|desktop|tablet)|desktop browser|light theme only|english locale only|render on desktop and mobile|mobile collapse|canonical platform contract|next\.js rsc|tailwind v4|qa.{0,100}desktop\s*(?:\+|and|&)\s*mobile|render.{0,100}desktop\s*(?:\+|and|&)\s*mobile|screenshots?.{0,100}desktop.{0,80}mobile|dark mode tokens|both modes|\b(?:1280|1920)px\b',text,re.I))
  checks['no_invented_interface_target']=not bool(re.search(r'≤\s*\d+\s*(?:clicks?|steps?|seconds?)|\bfastest\s+(?:way|method|path)|\b\d+(?:\.\d+)?x\s+(?:faster|better)|\b(?:lcp|inp|cls)\s*[<≤=].{0,20}\d',text,re.I))
  checks['no_plausible_perf_as_evidence']=('plausibl' not in text.lower()) or bool(re.search(r'plausibl.{0,40}(not evidence|is not evidence|unverified)',text,re.I))
 if name=='motion':
  checks['no_invented_public_metric']=not bool(re.search(r'\b(?:100% deterministic|\d+(?:\.\d+)?(?:%|×|x)\s+(?:faster|better|deterministic|accurate|reliable))',text,re.I))
  checks['no_invented_org_descriptor']=not bool(re.search(r'\binversion labs (?:is|does|builds|creates|provides)\b|\binversion labs is (?:an? )?(?:(?:precision|software|ai|technology|engineering)\s+){0,3}(?:firm|company|platform|system|studio|agency|operating system)\b',text,re.I))
  checks['single_primary_owner']=len(re.findall(r'primary owner',text,re.I))==1
  checks['ledger_no_aesthetic_keep']=not any(('keep' in line.lower() and re.search(r'engineer(?:ed)? rhythm|brand rhythm|premium feel|feels resolved|establish(?:es)? precision|reveal(?:s)? precision|subtle dynamism|keep it alive|signals? activation|resolved state|resolution and confidence|establish(?:es)? confidence|demonstrate(?:s)? precision|precision and resolution|add depth',line,re.I)) for line in text.splitlines())
  checks['no_unverified_loop_keep']=not any(('keep' in line.lower() and re.search(r'pulse|breathe|drift|shimmer|oscillat|beat-sync|beat sync|loop',line,re.I) and not re.search(r'(supplied|verified).{0,120}(audio|cue|state|event|continuity)|(audio|cue|state|event|continuity).{0,120}(supplied|verified)',line,re.I)) for line in text.splitlines())
  checks['ledger_has_basis']=bool(re.search(r'motion purpose ledger.{0,600}\bbasis\b',text,re.I|re.S))
  checks['motion_precedence_exact']=bool(re.search(r'precedence:.{0,120}brief/brand truth.{0,120}safety/legal/claims.{0,120}hyperframes technical contract.{0,160}taste',text,re.I|re.S))
  checks['ledger_no_fake_supplied']=not bool(re.search(r'basis\s*=\s*SUPPLIED\s*\[',text,re.I))
  checks['proposed_no_fake_state']=not any(('keep' in line.lower() and 'proposed' in line.lower() and re.search(r'activation state|activated|ready state|completion state|show .*state',line,re.I)) for line in text.splitlines())
  checks['audience_not_fake_supplied']=not bool(re.search(r'audience assumption:\s*supplied',text,re.I))
  checks['technical_contract_not_creative_basis']=not any(('keep' in line.lower() and re.search(r'(?:verified|supplied)\s*\[[^\]]*(?:render|check|test|technical|hyperframes|taste|filter)[^\]]*\]',line,re.I)) for line in text.splitlines())
  checks['ledger_status_closed_enum']=not bool(re.search(r'basis\s*=\s*(?:internal|assumed|approved|unknown)\s*\[',text,re.I))
  checks['audience_assumption_not_fake_supplied']=not bool(re.search(r'audience assumption:[^\n]*supplied',text,re.I))
  checks['no_invented_render_format']=not bool(re.search(r'\b(?:720p|1080p|1440p|2160p|4k|8k|24\s*fps|25\s*fps|30\s*fps|60\s*fps|16:9|9:16|4:5|1:1|1920x1080|1080x1920)\b',text,re.I))
  checks['render_duration_uses_supplied_8s']=bool(re.search(r'duration\s*=\s*SUPPLIED\[[^\]]*(?:8\s*(?:s|sec|second)|8-second)[^\]]*\]',text,re.I))
  checks['attention_budget_no_fake_percent']=not bool(re.search(r'attention budget[^\n]*%',text,re.I))
  checks['sustained_motion_basis_none']=bool(re.search(r'sustained-motion-basis\s*=\s*NONE',text,re.I))
  checks['product_state_basis_none']=bool(re.search(r'product-state-basis\s*=\s*NONE',text,re.I))
  checks['no_unsupplied_brand_promise']=not bool(re.search(r"brand(?:’s|\'s|s) promise|brand promise",text,re.I))
  checks['identity_only_when_no_product_state']=not bool(re.search(r'\b(?:new |product )?capabilit(?:y|ies)\b|\bvalue proposition\b|\bproblem(?:/|\s+and\s+|\s*→\s*)solution\b|\bintervention\b',text,re.I))
  checks['none_scope_not_ledger_basis']=not any(('KEEP' in line.upper() and re.search(r'Basis[^|\n]*NONE',line,re.I)) for line in text.splitlines())
  checks['visual_craft_not_truth_evidence']=not bool(re.search(r'visual authority.{0,40}is evidence|craft.{0,40}is evidence.{0,80}product',text,re.I))
  checks['no_proposed_product_story']=not bool(re.search(r'product capability|value proposition|problem state|resolved state|intervention in action|demonstrat(?:e|es|ing) (?:the )?(?:product|capability)',text,re.I))
  checks['unknown_audio_not_na']=not bool(re.search(r'audio\s*=\s*(?:NONE|N/?A)',text,re.I))
  checks['unknown_audio_not_absent']=not bool(re.search(r'no audio(?:/caption)? sync required|audio(?: sync)?\s*[:=]?\s*(?:NONE|N/?A)\b|audio[^.\n]{0,60}not required',text,re.I))
  checks['audio_unsupplied_stays_unknown']=bool(re.search(r'audio\s*=\s*UNKNOWN',text,re.I))
  checks['unknown_aspect_pending_scope']=bool(re.search(r'aspect-dependent evidence\s*=\s*PENDING SCOPE',text,re.I))
  checks['unknown_resolution_pending_scope']=bool(re.search(r'resolution-dependent evidence\s*=\s*PENDING SCOPE',text,re.I))
  checks['unknown_audio_pending_scope']=bool(re.search(r'audio-dependent evidence\s*=\s*PENDING SCOPE',text,re.I))
  checks['no_resolution_claim_when_unknown']=not bool(re.search(r'(?:type|text).{0,60}(?:legible|readable).{0,60}(?:intended|unknown) resolution|compression.{0,80}resolution\s*=\s*UNKNOWN',text,re.I))
  allowed_jobs=('REVEAL_INFO','DIRECT_HIERARCHY','DEMONSTRATE_STATE','CONTINUITY','CAUSE_EFFECT','SYNC_REAL_CUE','PAUSE_READABILITY')
  keep_lines=[line for line in text.splitlines() if 'KEEP' in line.upper() and 'KEEP/DELETE' not in line.upper()]
  allowed_no_authority=('REVEAL_INFO','DIRECT_HIERARCHY','PAUSE_READABILITY')
  checks['no_authority_job_subset']=all(any(job in line.upper() for job in allowed_no_authority) for line in keep_lines)
  checks['ledger_jobs_closed_enum']=all(any(job in line.upper() for job in allowed_jobs) for line in keep_lines) and bool(keep_lines)
  checks['proposed_not_state_or_cue']=not any(('PROPOSED' in line.upper() and ('DEMONSTRATE_STATE' in line.upper() or 'SYNC_REAL_CUE' in line.upper()) and 'KEEP' in line.upper()) for line in keep_lines)
  checks['no_state_job_without_authority']=not any((('DEMONSTRATE_STATE' in line.upper() or 'CAUSE_EFFECT' in line.upper()) and 'KEEP' in line.upper()) for line in keep_lines)
  checks['static_hold_uses_pause_job']=not any(('KEEP' in line.upper() and re.search(r'hold static|static hold|holds? static',line,re.I) and 'PAUSE_READABILITY' not in line.upper()) for line in keep_lines)
  checks['continuity_has_boundary']=not any(('KEEP' in line.upper() and 'CONTINUITY' in line.upper() and not re.search(r'scene|seam|cut|handoff|boundary',line,re.I)) for line in keep_lines)
  checks['static_background_not_ledger_keep']=not any(('KEEP' in line.upper() and re.search(r'background.{0,80}(?:static|remains static)|(?:static|remains static).{0,80}background',line,re.I)) for line in keep_lines)
 checks['bounded_handoff']=len(text.split()) <= 700
 results[name]=checks
 print(name, f'{sum(checks.values())}/{len(checks)}', checks, flush=True)
(OUT/'final-results.json').write_text(json.dumps(results,indent=2)+'\n')
