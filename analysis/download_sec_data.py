"""
Download SEC Form D data sets for 2008-2021
Correct URL: https://www.sec.gov/files/structureddata/data/form-d-data-sets/
"""

import os
import requests
import zipfile
import time
from pathlib import Path

BASE_DIR = Path("/Users/bhumikamarmat/sec filings")

HEADERS = {
    "User-Agent": "Z5Capital bhumikamarmat@gmail.com",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "*/*",
}

BASE_URL = "https://www.sec.gov/files/structureddata/data/form-d-data-sets"


def download_file(url: str, dest: Path) -> bool:
    """Download a file from SEC"""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=60, stream=True)
        content_type = resp.headers.get('content-type', '')
        
        if resp.status_code == 200 and 'html' not in content_type.lower():
            with open(dest, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            size_mb = os.path.getsize(dest) / (1024 * 1024)
            print(f"  ✓ {dest.name} ({size_mb:.1f} MB)")
            return True
        else:
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def extract_zip(zip_path: Path, dest_dir: Path):
    """Extract zip file"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(dest_dir)
        return True
    except Exception as e:
        print(f"  ✗ Extract error: {e}")
        return False


def main():
    years = list(range(2008, 2022))  # 2008-2021
    
    print("=" * 60)
    print("SEC Form D Data Downloader (2008-2021)")
    print("=" * 60)
    
    # Some quarters have _0 suffix (SEC inconsistency)
    # Try both patterns for each quarter
    success = 0
    failed = 0
    
    for year in years:
        print(f"\n--- {year} ---")
        
        year_dir = BASE_DIR / str(year)
        
        # Check if we already have this year's data
        if year_dir.exists() and any(year_dir.rglob("*.tsv")):
            print(f"  Already have {year} data, skipping")
            success += 1
            continue
        
        year_dir.mkdir(exist_ok=True)
        year_ok = True
        
        for q in range(1, 5):
            q_dir_name = f"{year}Q{q}_d"
            q_dir = year_dir / q_dir_name
            
            if q_dir.exists() and any(q_dir.rglob("*.tsv")):
                print(f"  Q{q}: already exists")
                continue
            
            # Try different URL patterns
            patterns = [
                f"{BASE_URL}/{year}q{q}_d.zip",
                f"{BASE_URL}/{year}q{q}_d_0.zip",
            ]
            
            downloaded = False
            for url in patterns:
                zip_path = BASE_DIR / f"{year}Q{q}_d.zip"
                if download_file(url, zip_path):
                    q_dir.mkdir(parents=True, exist_ok=True)
                    extract_zip(zip_path, q_dir)
                    os.remove(zip_path)  # Clean up zip
                    downloaded = True
                    break
                # Clean up failed download
                if zip_path.exists():
                    os.remove(zip_path)
            
            if not downloaded:
                print(f"  ✗ Q{q}: all URL patterns failed")
                year_ok = False
            
            time.sleep(0.5)  # Rate limit
        
        if year_ok:
            success += 1
        else:
            failed += 1
        
        time.sleep(0.5)
    
    print(f"\n{'=' * 60}")
    print(f"Done: {success} years OK, {failed} failed")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
