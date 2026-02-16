"""
Run complete data pipeline: loading + cleaning
"""

import sys
from pathlib import Path

# Add analysis directory to path
sys.path.insert(0, str(Path(__file__).parent))

from data_loader import FormDDataLoader
from data_cleaning import FormDDataCleaner

def main():
    base_path = "/Users/bhumikamarmat/sec filings"
    
    print("=" * 70)
    print("SEC FORM D ANALYSIS PIPELINE")
    print("=" * 70)
    
    # Step 1: Load data
    print("\n###STEP 1: LOADING DATA###")
    loader = FormDDataLoader(base_path)
    master_data = loader.load_all_data()
    
    # Save master data
    data_dir = Path(base_path) / "data"
    loader.save_master_data(str(data_dir))
    
    # Step 2: Clean data
    print("\n###STEP 2: CLEANING DATA###")
    cleaner = FormDDataCleaner(master_data)
    cleaned_data = cleaner.clean_all_tables()
    
    # Save cleaned data
    cleaner.save_cleaned_data(str(data_dir))
    
    # Step 3: Show preview
    print("\n" + "=" * 70)
    print("ANALYTICAL DATASET PREVIEW")
    print("=" * 70)
    analytical = cleaned_data['analytical']
    
    preview_cols = [
        'entity_name_clean', 'sector', 'state', 'region',
        'total_offering_amount', 'total_amount_sold', 'deal_size_category',
        'filing_date', 'is_fund', 'is_follow_on', 'is_recent'
    ]
    
    print(analytical[preview_cols].head(20).to_string())
    
    print("\n" + "=" * 70)
    print("PIPELINE COMPLETE!")
    print("=" * 70)
    print(f"Analytical dataset: {len(analytical):,} offerings")
    print(f"Data saved to: {data_dir}")
    print(f"Date range: {analytical['filing_date'].min()} to {analytical['filing_date'].max()}")
    
    # Summary stats
    print("\nKey Statistics:")
    print(f"  Total capital raised: ${analytical['total_amount_sold'].sum() / 1e9:.2f}B")
    print(f"  Median offering size: ${analytical['total_offering_amount'].median() / 1e6:.1f}M")
    print(f"  Investment funds: {analytical['is_fund'].sum():,}")
    print(f"  Operating companies: {(~analytical['is_fund']).sum():,}")
    print(f"  US-based: {analytical['is_us'].sum():,}")
    print(f"  Recent filings (18mo): {analytical['is_recent'].sum():,}")
    

if __name__ == "__main__":
    main()
