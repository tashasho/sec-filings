import csv
import json
import re
import os

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

csv_file = '/Users/bhumikamarmat/Downloads/ycombinator-2026-04-07.csv'
checkpoint_file = 'data/step2_checkpoint.json'

with open(checkpoint_file) as f:
    checkpoint = json.load(f)

# build an index
founder_map = {}
for slug, founders in checkpoint.items():
    if not founders: continue
    for f in founders:
        name = f.get('name', '').lower().strip()
        if name:
            founder_map[name] = {
                'bio': f.get('bio', ''),
                'linkedin': f.get('linkedin', ''),
                'title': f.get('title', ''),
                'company_slug': slug
            }

found_count = 0
total_count = 0

with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        total_count += 1
        name = row['_coName_18olp_472'].lower().strip()
        if name in founder_map:
            found_count += 1

print(f"Matched {found_count} out of {total_count} founders using checkpoint.")
