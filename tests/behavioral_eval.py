from pathlib import Path
import json, re, urllib.request

ROOT = Path('/Users/knowurknot/inversion-labs-skills')
UP = Path('/Users/knowurknot/.agents/skills')
OUT = ROOT / 'evals' / 'local-qwen'
OUT.mkdir(parents=True, exist_ok=True)

SCENARIOS = {
    'interface': {
        'files': [UP/'taste/SKILL.md', UP/'design-taste-frontend/SKILL.md', UP/'impeccable/SKILL.md'],
        'overlay': ROOT/'skills/inversion-interface-craft/SKILL.md',
        'prompt': (ROOT/'evals/baseline/prompt-interface.txt').read_text(),
        'checks': {
            'impeccable_primary': r'impeccable.{0,80}(primary|owner)|primary.{0,80}impeccable',
            'taste_dashboard_scope': r'design-taste-frontend.{0,180}(not|do not|exclude|out.of.scope).{0,100}(dashboard|product)|dashboard.{0,180}(not|do not|exclude|out.of.scope).{0,100}design-taste-frontend',
            'precedence': r'preceden|conflict|wins|override',
            'bounded_qa': r'(one|1).{0,50}(inspection|pass|round).{0,120}(one|1).{0,50}(confirm|confirmation)|bounded',
            'evidence': r'(screenshot|render).{0,100}(keyboard|focus|contrast|responsive|state|test)',
        },
    },
    'motion': {
        'files': [UP/'taste/SKILL.md', UP/'hyperframes/SKILL.md', UP/'hyperframes-core/SKILL.md', UP/'hyperframes-creative/SKILL.md', UP/'impeccable/SKILL.md'],
        'overlay': ROOT/'skills/inversion-motion-craft/SKILL.md',
        'prompt': (ROOT/'evals/baseline/prompt-motion.txt').read_text(),
        'checks': {
            'hyperframes_primary': r'hyperframes.{0,80}(primary|owner)|primary.{0,80}hyperframes',
            'technical_precedence': r'(technical|runtime|render|seek.safe|determin).{0,120}(wins|preced|override|contract)',
            'impeccable_conditional': r'impeccable.{0,180}(only|if|when).{0,120}(ui|interface|product)',
            'no_idle_wobble': r'(no|ban|avoid).{0,80}(idle|wobble|breathe|drift|pulse)|motion.{0,80}(perform|job|purpose)',
            'render_evidence': r'(render|check).{0,120}(frame|seam|clip|sync|evidence|verify)',
        },
    },
}

def call(prompt):
    body = json.dumps({
        'model':'qwen3.5-defiant-fable:latest',
        'messages':[{'role':'user','content':prompt}],
        'stream':False,
        'think':False,
        'options':{'temperature':0,'num_predict':1800,'num_ctx':65536},
    }).encode()
    req = urllib.request.Request('http://127.0.0.1:11434/api/chat', data=body, headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req, timeout=300) as r:
        d=json.load(r)
    return d['message']['content']

def grade(text, checks):
    return {k: bool(re.search(rx, text, flags=re.I|re.S)) for k,rx in checks.items()}

results={}
for name,cfg in SCENARIOS.items():
    upstream='\n\n'.join(f'### UPSTREAM {p.parent.name}\n{p.read_text()}' for p in cfg['files'])
    base_prompt=f'''You are evaluating skill composition. Treat the following upstream SKILL.md texts as authoritative. Do not edit files.\n\n{upstream}\n\nSCENARIO\n{cfg['prompt']}\n\nAnswer the scenario directly.'''
    post_prompt=base_prompt + f'''\n\nADDITIONAL INVERSION LABS OVERLAY (authoritative for cross-skill ownership and conflict resolution)\n{cfg['overlay'].read_text()}\n\nRe-answer the scenario using the overlay to compose, not replace, upstream skills.'''
    for phase,prompt in [('baseline',base_prompt),('post',post_prompt)]:
        text=call(prompt)
        (OUT/f'{name}-{phase}.txt').write_text(text+'\n')
        scores=grade(text,cfg['checks'])
        results[f'{name}-{phase}']={'passed':sum(scores.values()),'total':len(scores),'checks':scores}
        print(f'{name}-{phase}: {sum(scores.values())}/{len(scores)} {scores}', flush=True)
(OUT/'results.json').write_text(json.dumps(results,indent=2)+'\n')
