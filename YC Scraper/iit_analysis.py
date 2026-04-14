import json
from collections import Counter
import os

def analyze_iit_founders():
    data_path = os.path.join(os.path.dirname(__file__), "data", "step3_iit_founders_csv.json")
    if not os.path.exists(data_path):
        print("Data not found!")
        return

    with open(data_path, "r") as f:
        founders = json.load(f)

    print(f"Total IIT Founders analyzed: {len(founders)}")

    # Campus breakdown
    campuses = [f.get("iit_campus") for f in founders if f.get("iit_campus")]
    campus_counts = Counter(campuses)
    print("\n--- IIT Campuses Producing Most Startups ---")
    for campus, count in campus_counts.most_common():
        print(f"{campus}: {count}")

    # Graduation Year Patterns
    years = [f.get("grad_year") for f in founders if f.get("grad_year") and f.get("grad_year").isdigit()]
    year_counts = Counter(years)
    print("\n--- Graduation Year Patterns ---")
    
    # Sort by year
    sorted_years = sorted(year_counts.items(), key=lambda x: int(x[0]))
    for y, count in sorted_years:
        print(f"Year {y}: {count} founders")

    # Degrees
    degrees = [f.get("degree", "").lower() for f in founders if f.get("degree")]
    print("\n--- Common Degrees ---")
    deg_counter = Counter(degrees)
    for deg, count in deg_counter.most_common(10):
        if deg.strip():
            print(f"{deg}: {count}")

    # Industries
    industries = [f.get("company_industry") for f in founders if f.get("company_industry")]
    ind_counts = Counter(industries)
    print("\n--- Top Industries ---")
    for ind, count in ind_counts.most_common(10):
        print(f"{ind}: {count}")

    artifact_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".gemini", "antigravity", "brain", "d1698179-f3e0-4219-ba80-e0f8983563eb", "iit_analysis_results.md")
    with open(artifact_path, "w") as f:
        f.write("# IIT Alumni YC Founders Analysis\n\n")
        f.write(f"Total IIT Founders configured from CSV match: {len(founders)}\n\n")
        
        f.write("## 🏫 IIT Campuses Producing Most Startups\n")
        for campus, count in campus_counts.most_common():
            f.write(f"- **{campus}**: {count}\n")
            
        f.write("\n## 🎓 Graduation Year Patterns\n")
        f.write("Does industry experience matter before starting a YC company? Here are the graduation years:\n")
        for y, count in sorted_years:
            f.write(f"- **{y}**: {count} founders\n")
            
        f.write("\n## 📚 Common Degrees\n")
        for deg, count in deg_counter.most_common(10):
            if deg.strip():
                f.write(f"- {deg}: {count}\n")
                
        f.write("\n## 💼 Top Industries\n")
        for ind, count in ind_counts.most_common(10):
            f.write(f"- {ind}: {count}\n")

if __name__ == "__main__":
    analyze_iit_founders()
