import csv
import json
import os
from pathlib import Path

from yc_scraper import (
    detect_indian_bachelor, 
    extract_education_details, 
    generate_excel,
    OUTPUT_FILE
)

def process_csv_and_generate_sheet():
    csv_file = '/Users/bhumikamarmat/Downloads/ycombinator-2026-04-07.csv'
    checkpoint_file = Path('data/step2_checkpoint.json')
    step1_file = Path('data/step1_companies.json')
    
    with open(checkpoint_file) as f:
        checkpoint = json.load(f)
        
    with open(step1_file) as f:
        all_companies_meta = json.load(f)
        
    founder_map = {}
    for slug, founders in checkpoint.items():
        if not founders: continue
        for f in founders:
            name = f.get('name', '').lower().strip()
            if name:
                founder_map[name] = {
                    'bio': f.get('bio', ''),
                    'linkedin': f.get('linkedin', ''),
                    'twitter': f.get('twitter', ''),
                    'title': f.get('title', ''),
                    'company_slug': slug
                }

    all_csv_companies = {}
    indian_founders = []
    iit_founders = []

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name_raw = row.get('_coName_18olp_472', '').strip()
            name = name_raw.lower()
            
            # Extract batch and company from CSV if we want, or rely on matched data
            # The CSV row contains batches like F25, S25 etc.
            batch = row.get('pill', '').strip()
            
            if name in founder_map:
                f_data = founder_map[name]
                slug = f_data['company_slug']
                
                # Fetch company details
                c_meta = all_companies_meta.get(slug, {})
                company_name = c_meta.get('name', '')
                industry = c_meta.get('industry', '')
                subindustry = c_meta.get('subindustry', '')
                one_liner = c_meta.get('one_liner', '')
                c_status = c_meta.get('status', '')
                c_stage = c_meta.get('stage', '')
                team_size = c_meta.get('team_size', '')
                location = c_meta.get('all_locations', '')
                tags = c_meta.get('tags', '')
                if isinstance(tags, list):
                    tags = ", ".join(tags)
                    c_meta['tags'] = tags
                yc_url = c_meta.get('url', f"https://www.ycombinator.com/companies/{slug}")
                website = c_meta.get('website', '')
                
                # Prepare company dict for Excel generation requirements
                if slug not in all_csv_companies:
                    all_csv_companies[slug] = c_meta
                    all_csv_companies[slug]['batch'] = batch  # Overwrite batch from CSV
                    all_csv_companies[slug]['founders'] = checkpoint[slug]
                else:
                    all_csv_companies[slug]['batch'] = batch

                bio = f_data['bio']
                long_desc = c_meta.get("long_description", "")
                search_text = f"{bio} {long_desc}"
                
                if not detect_indian_bachelor(search_text):
                    continue
                
                edu = extract_education_details(search_text)
                
                record = {
                    "name": name_raw,
                    "bio": bio,
                    "company": company_name,
                    "batch": batch,
                    "title": f_data['title'],
                    "linkedin": f_data['linkedin'],
                    "twitter": f_data['twitter'],
                    "university": edu["university"],
                    "degree": edu["degree"],
                    "grad_year": edu["grad_year"],
                    "is_iit": edu["is_iit"],
                    "iit_campus": edu["iit_campus"],
                    "company_website": website,
                    "company_industry": industry,
                    "company_subindustry": subindustry,
                    "company_one_liner": one_liner,
                    "company_status": c_status,
                    "company_stage": c_stage,
                    "team_size": team_size,
                    "location": location,
                    "tags": tags,
                    "yc_url": yc_url,
                }
                
                indian_founders.append(record)
                if edu['is_iit']:
                    iit_founders.append(record)
                    
    print(f"Extracted {len(indian_founders)} Indian-origin founders.")
    print(f"Extracted {len(iit_founders)} IIT alumni founders.")
    
    # Generate Excel sheet using the module function
    print("Generating updated Excel...")
    generate_excel(all_csv_companies, indian_founders, iit_founders)
    
    # Dump the filtered datasets for the analysis script
    with open('data/step3_iit_founders_csv.json', 'w') as f:
        json.dump(iit_founders, f)
        
    print("Done!")

if __name__ == '__main__':
    process_csv_and_generate_sheet()
