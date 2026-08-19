from pathlib import Path
import json,re,urllib.request
ROOT=Path('/Users/knowurknot/inversion-labs-skills'); OUT=ROOT/'evals/local-qwen'; OUT.mkdir(parents=True,exist_ok=True)
SK=ROOT/'skills'
PACKS={
'director':'\n\n'.join((SK/n/'SKILL.md').read_text() for n in ['inversion-creative-director','inversion-interface-craft','inversion-motion-craft','inversion-creative-critic']),
'critic':'\n\n'.join((SK/n/'SKILL.md').read_text() for n in ['inversion-creative-critic','inversion-interface-craft','inversion-motion-craft','inversion-creative-director']),
}

def call(prompt):
    body=json.dumps({'model':'qwen3.5-defiant-fable:latest','messages':[{'role':'user','content':prompt}],'stream':False,'think':False,'options':{'temperature':0,'num_predict':1800,'num_ctx':32768}}).encode()
    req=urllib.request.Request('http://127.0.0.1:11434/api/chat',data=body,headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req,timeout=300) as r:return json.load(r)['message']['content']

cases={
'director': (ROOT/'evals/baseline/prompt-director.txt').read_text(),
'critic': (ROOT/'evals/baseline/prompt-critic.txt').read_text(),
}
results={}
for name,scenario in cases.items():
    prompt=f'''Active skill: inversion-creative-{name}. Use that skill's required output shape. Other pack skills are support only and must not replace the active skill's role. Do not restate the skills. Answer in <=600 words.\n\n{PACKS[name]}\n\nSCENARIO\n{scenario}\n'''
    text=call(prompt); (OUT/f'{name}-final.txt').write_text(text+'\n')
    if name=='director':
        checks={
            'landing_interface_owner': bool(re.search(r'(landing|marketing).{0,180}inversion-interface-craft|inversion-interface-craft.{0,180}(landing|marketing)',text,re.I|re.S)),
            'dashboard_interface_owner': bool(re.search(r'dashboard.{0,180}inversion-interface-craft|inversion-interface-craft.{0,180}dashboard',text,re.I|re.S)),
            'film_motion_owner': bool(re.search(r'(film|video|motion).{0,180}inversion-motion-craft|inversion-motion-craft.{0,180}(film|video|motion)',text,re.I|re.S)),
            'one_owner_language': bool(re.search(r'one primary|exactly one|single (?:primary|production) owner',text,re.I)) or ('ownership table' in text.lower() and '+' not in '\n'.join(line for line in text.splitlines() if '→' in line or '->' in line)),
            'proposed_internal_spine': bool(re.search(r'spine.{0,80}proposed internal|proposed internal.{0,80}spine',text,re.I)),
            'shared_thesis_not_same_layout': bool(re.search(r'(shared thesis|shared spine|shared[:=]|coherent identity).{0,600}(not identical|different composition|medium-specific|own composition|realization\s*=\s*delegated)|functions=.{0,300}realization\s*=\s*delegated',text,re.I|re.S)),
            'precedence': bool(re.search(r'brief.{0,300}safety.{0,300}(technical|runtime|medium).{0,400}taste',text,re.I|re.S)),
            'evidence_states': bool(re.search(r'evidence (?:states?|status).{0,100}(blocked|unverified)',text,re.I|re.S)),
            'unknown_scope_not_invented': not bool(re.search(r'\b(?:16:9|9:16|1080p|desktop and mobile|light and dark|lcp\s*[<≤])',text,re.I)),
            'no_cross_media_constraint_leak': not bool(re.search(r'(?:operator|dashboard|page|package)[^\n]{0,120}(?:within\s*\d+\s*seconds?|<\s*\d+\s*s|\d+\s*s\s*to)|(?:seconds total across artifacts|film cue)',text,re.I)),
            'shared_attention_qualitative': not bool(re.search(r'shared attention budget[^\n]*(?:\d+\s*s|seconds?|<\s*\d+|\d+%)',text,re.I)),
            'shared_motif_not_motion_rule': not bool(re.search(r'(?:shared|motif)[^\n]{0,160}(?:pulse|drift|breathe|live state|animation cue|motion glyph)',text,re.I)),
            'bounded_qa': bool(re.search(r'(one|1).{0,80}inspection.{0,120}(batch|batched).{0,120}confirm.{0,120}stop',text,re.I|re.S)),
            'no_child_mechanics': not bool(re.search(r'motion purpose ledger|job=|data-start|design_variance|motion_intensity|hyperframes (?:check|snapshot|render)|sustained-motion-basis|product-state-basis|qa: inspect resolved|qa: one rendered|\b(?:16:9|9:16|1080p)\b',text,re.I)),
            'acceptance_blocked': bool(re.search(r'acceptance:.{0,100}blocked.{0,120}inversion-creative-critic',text,re.I|re.S)),
            'no_director_pass': not bool(re.search(r'(?:decision|acceptance):\s*PASS\b',text,re.I)),
            'compact': len(text.split())<=700,
        }
    else:
        checks={
            'decision_blocked_without_artifacts': bool(re.search(r'\bBLOCKED\b',text,re.I)),
            'no_invented_verified_defect': not bool(re.search(r'\|\s*VERIFIED(?:\s*/|\s*\|)',text,re.I)),
            'claims_not_inferred': not bool(re.search(r'(claims?|capabilit(?:y|ies))[^\n|]{0,80}\|\s*INFERRED|(?:claims?|capabilit(?:y|ies))[^\n]{0,120}(?:state|is|are)\s+INFERRED',text,re.I)),
            'technical_not_inferred': not bool(re.search(r'(responsive|contrast|accessibility|render|sync|seam|performance|hierarchy|required states?)[^\n|]{0,120}\|\s*INFERRED|hierarchy[^\n]{0,100}INFERRED|INFERRED[^\n]{0,100}hierarchy',text,re.I)),
            'no_invented_evidence_scope': not bool(re.search(r'at least (?:one|two) (?:device|breakpoint|focus|caption)|two device classes|both themes|light and dark|audio, captions|audio and captions|loading, error, hover|loading, error|caption sync|responsive breakpoints|\b(?:16:9|9:16|1080p)\b',text,re.I)),
            'no_pseudo_observation': not bool(re.search(r'no explicit thesis detected|appears to rely|inferred to be present|detected.{0,80}(hierarchy|spine|claim)',text,re.I)),
            'evidence_states': all(x in text.upper() for x in ['VERIFIED','INFERRED','UNVERIFIED','BLOCKED']),
            'separates_inference': bool(re.search(r'INFERRED.{0,400}(aesthetic|generic|identity|judgment|taste|risk)|(?:aesthetic|generic|risk).{0,400}INFERRED',text,re.I|re.S)),
            'medium_specific': bool(re.search(r'(web|interface).{0,350}(video|film|motion).{0,350}(identity|thesis|palette|type|voice|motif)',text,re.I|re.S)),
            'not_identical_composition': bool(re.search(r'not (?:require )?identical|should not (?:become|look like)|different composition|without identical composition|identical composition (?:would|is|violates?)|no identical (?:motion|layout|composition)|neither should replicate',text,re.I)),
            'bounded_stop': bool(re.search(r'(inspection|inspect).{0,220}(batch|batched).{0,220}(confirmation|confirm).{0,220}(stop|re-open)',text,re.I|re.S)),
            'blocked_early_return_stops': (lambda m: bool(m) and not text[m.end():].strip())(re.search(r'(?im)^.*Stop:.*STOP.*$',text)),
            'compact': len(text.split())<=700,
        }
    results[name]=checks
    print(name,f'{sum(checks.values())}/{len(checks)}',checks,flush=True)
(OUT/'cross-medium-results.json').write_text(json.dumps(results,indent=2)+'\n')
