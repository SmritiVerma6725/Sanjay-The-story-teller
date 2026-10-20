import re
import json

with open('extension/translation/isl_translator.js', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'const SEED_LEXICON = Object\.freeze\(\{([\s\S]*?)\}\);\s*// Fast reverse', content)
if not match:
    print("Could not find SEED_LEXICON block")
    exit(1)

block = match.group(1)

# Find each entry: GLOSS: Object.freeze({ ... })
entries = re.findall(r'([A-Z_]+):\s*Object\.freeze\(\{([\s\S]*?)\}\)', block)

print(f"Total Gloss Keys parsed: {len(entries)}")

gloss_list = []
total_lemmas = 0
all_lemmas = []

for gloss, body in entries:
    anim_match = re.search(r'animationId:\s*[\'"]([^\'"]+)[\'"]', body)
    anim_id = anim_match.group(1) if anim_match else None
    
    lemmas_match = re.search(r'lemmas:\s*Object\.freeze\(\[([\s\S]*?)\]\)', body)
    if lemmas_match:
        raw_lemmas = lemmas_match.group(1)
        lemmas = [l.strip().strip("'").strip('"') for l in raw_lemmas.split(',') if l.strip()]
    else:
        lemmas = []
    
    desc_match = re.search(r'description:\s*[\'"]([^\'"]+)[\'"]', body)
    desc = desc_match.group(1) if desc_match else ""
    
    dur_match = re.search(r'defaultDurationMs:\s*(\d+)', body)
    dur = int(dur_match.group(1)) if dur_match else 0
    
    total_lemmas += len(lemmas)
    all_lemmas.extend(lemmas)
    
    gloss_list.append({
        "gloss": gloss,
        "animationId": anim_id,
        "durationMs": dur,
        "lemmas": lemmas,
        "description": desc
    })
    print(f"Gloss: {gloss:12} | Anim: {str(anim_id):26} | Lemmas ({len(lemmas)}): {lemmas}")

print(f"\nSummary:")
print(f"Total Glosses: {len(gloss_list)}")
print(f"Total Unique Lemmas/Phrases: {len(all_lemmas)} (unique: {len(set(all_lemmas))})")
