"""
Data Loading Module for SEC Form D Filings
Loads and consolidates quarterly TSV files from 2022-2025
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class FormDDataLoader:
    """
    Loads and consolidates SEC Form D filing data from multiple quarters
    """
    
    def __init__(self, base_path: str):
        """
        Initialize the data loader
        
        Args:
            base_path: Path to the directory containing Form D data
        """
        self.base_path = Path(base_path)
        self.data_files = {
            'submissions': 'FORMDSUBMISSION.tsv',
            'issuers': 'ISSUERS.tsv',
            'offerings': 'OFFERING.tsv',
            'recipients': 'RECIPIENTS.tsv',
            'related_persons': 'RELATEDPERSONS.tsv',
            'signatures': 'SIGNATURES.tsv'
        }
        
        # Storage for loaded data
        self.master_data: Dict[str, pd.DataFrame] = {}
        
    def get_available_quarters(self) -> List[Tuple[int, int]]:
        """
        Identify all available quarterly data directories
        
        Returns:
            List of (year, quarter) tuples
        """
        quarters = []
        
        # Look for quarterly directories (2024Q1_d, 2024Q2_d, etc.)
        for item in self.base_path.iterdir():
            if item.is_dir() and 'Q' in item.name and '_d' in item.name:
                try:
                    parts = item.name.replace('_d', '').split('Q')
                    year = int(parts[0])
                    quarter = int(parts[1])
                    quarters.append((year, quarter))
                except (ValueError, IndexError):
                    logger.warning(f"Skipping directory with unexpected format: {item.name}")
                    
        # Sort by year and quarter
        quarters.sort()
        return quarters
    
    def load_quarterly_data(self, year: int, quarter: int) -> Dict[str, pd.DataFrame]:
        """
        Load all TSV files for a specific quarter
        
        Args:
            year: Year (e.g., 2024)
            quarter: Quarter number (1-4)
            
        Returns:
            Dictionary of dataframes keyed by table type
        """
        quarter_dir = self.base_path / f"{year}Q{quarter}_d"
        
        if not quarter_dir.exists():
            raise FileNotFoundError(f"Quarter directory not found: {quarter_dir}")
        
        logger.info(f"Loading data for {year} Q{quarter}...")
        
        quarterly_data = {}
        
        for data_type, filename in self.data_files.items():
            file_path = quarter_dir / filename
            
            if not file_path.exists():
                logger.warning(f"File not found: {file_path}")
                continue
            
            try:
                # Load TSV with tab delimiter
                df = pd.read_csv(file_path, sep='\t', low_memory=False, encoding='utf-8')
                
                # Add metadata columns
                df['data_year'] = year
                df['data_quarter'] = quarter
                df['data_period'] = f"{year}Q{quarter}"
                
                quarterly_data[data_type] = df
                logger.info(f"  Loaded {data_type}: {len(df):,} rows")
                
            except Exception as e:
                logger.error(f"Error loading {file_path}: {str(e)}")
                raise
        
        return quarterly_data
    
    def load_all_data(self) -> Dict[str, pd.DataFrame]:
        """
        Load and consolidate all available quarterly data
        
        Returns:
            Dictionary of consolidated dataframes keyed by table type
        """
        logger.info("=" * 70)
        logger.info("SEC Form D Data Loader - Starting Data Consolidation")
        logger.info("=" * 70)
        
        quarters = self.get_available_quarters()
        
        if not quarters:
            raise ValueError("No quarterly data directories found")
        
        logger.info(f"Found {len(quarters)} quarters of data:")
        for year, quarter in quarters:
            logger.info(f"  - {year} Q{quarter}")
        
        # Initialize consolidated dataframes
        consolidated: Dict[str, List[pd.DataFrame]] = {
            key: [] for key in self.data_files.keys()
        }
        
        # Load each quarter and append to consolidated list
        for year, quarter in quarters:
            try:
                quarterly_data = self.load_quarterly_data(year, quarter)
                
                for data_type, df in quarterly_data.items():
                    consolidated[data_type].append(df)
                    
            except Exception as e:
                logger.error(f"Failed to load {year} Q{quarter}: {str(e)}")
                continue
        
        # Concatenate all quarters for each table type
        logger.info("\n" + "=" * 70)
        logger.info("Consolidating data across all quarters...")
        logger.info("=" * 70)
        
        for data_type, df_list in consolidated.items():
            if df_list:
                master_df = pd.concat(df_list, ignore_index=True)
                self.master_data[data_type] = master_df
                
                logger.info(f"{data_type.upper()}:")
                logger.info(f"  Total rows: {len(master_df):,}")
                logger.info(f"  Date range: {master_df['data_period'].min()} to {master_df['data_period'].max()}")
                logger.info(f"  Columns: {len(master_df.columns)}")
                
        return self.master_data
    
    def validate_schema(self, df: pd.DataFrame, table_type: str) -> Dict[str, any]:
        """
        Validate data schema and quality for a specific table
        
        Args:
            df: DataFrame to validate
            table_type: Type of table (submissions, issuers, etc.)
            
        Returns:
            Dictionary of validation results
        """
        validation_results = {
            'table_type': table_type,
            'row_count': len(df),
            'column_count': len(df.columns),
            'missing_values': {},
            'duplicate_keys': 0,
            'data_types': {},
            'issues': []
        }
        
        # Check for missing values
        missing = df.isnull().sum()
        validation_results['missing_values'] = missing[missing > 0].to_dict()
        
        # Check for duplicates based on primary key
        if table_type == 'submissions':
            duplicates = df['ACCESSIONNUMBER'].duplicated().sum()
            validation_results['duplicate_keys'] = duplicates
            if duplicates > 0:
                validation_results['issues'].append(f"Found {duplicates} duplicate accession numbers")
        
        elif table_type in ['issuers', 'offerings']:
            duplicates = df['ACCESSIONNUMBER'].duplicated().sum()
            validation_results['duplicate_keys'] = duplicates
            if duplicates > 0:
                validation_results['issues'].append(f"Found {duplicates} duplicate accession numbers")
        
        # Check data types
        validation_results['data_types'] = df.dtypes.astype(str).to_dict()
        
        return validation_results
    
    def generate_data_quality_report(self) -> str:
        """
        Generate a comprehensive data quality report
        
        Returns:
            Formatted report string
        """
        if not self.master_data:
            return "No data loaded. Please run load_all_data() first."
        
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("SEC FORM D DATA QUALITY REPORT")
        report_lines.append("=" * 80)
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        
        for table_type, df in self.master_data.items():
            report_lines.append(f"\n{'=' * 80}")
            report_lines.append(f"TABLE: {table_type.upper()}")
            report_lines.append(f"{'=' * 80}")
            
            validation = self.validate_schema(df, table_type)
            
            report_lines.append(f"Total Rows: {validation['row_count']:,}")
            report_lines.append(f"Total Columns: {validation['column_count']}")
            report_lines.append(f"Duplicate Keys: {validation['duplicate_keys']}")
            
            if validation['missing_values']:
                report_lines.append("\nMissing Values:")
                for col, count in sorted(validation['missing_values'].items(), 
                                        key=lambda x: x[1], reverse=True)[:10]:
                    pct = (count / validation['row_count']) * 100
                    report_lines.append(f"  {col}: {count:,} ({pct:.1f}%)")
            else:
                report_lines.append("\nMissing Values: None")
            
            if validation['issues']:
                report_lines.append("\nData Quality Issues:")
                for issue in validation['issues']:
                    report_lines.append(f"  - {issue}")
        
        report_lines.append("\n" + "=" * 80)
        report_lines.append("END OF REPORT")
        report_lines.append("=" * 80)
        
        return "\n".join(report_lines)
    
    def save_master_data(self, output_dir: str):
        """
        Save consolidated master data to CSV files
        
        Args:
            output_dir: Directory to save the CSV files
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"\nSaving master data to {output_path}...")
        
        for table_type, df in self.master_data.items():
            file_path = output_path / f"master_{table_type}.csv"
            df.to_csv(file_path, index=False)
            logger.info(f"  Saved {table_type}: {file_path}")
            logger.info(f"    Rows: {len(df):,}, Size: {file_path.stat().st_size / 1024 / 1024:.2f} MB")


def main():
    """
    Main function to demonstrate data loading
    """
    # Initialize loader
    base_path = "/Users/bhumikamarmat/sec filings"
    loader = FormDDataLoader(base_path)
    
    # Load all data
    master_data = loader.load_all_data()
    
    # Generate quality report
    print("\n")
    quality_report = loader.generate_data_quality_report()
    print(quality_report)
    
    # Save quality report
    reports_dir = Path(base_path) / "reports"
    reports_dir.mkdir(exist_ok=True)
    
    report_file = reports_dir / "data_quality_report.txt"
    with open(report_file, 'w') as f:
        f.write(quality_report)
    print(f"\n✓ Quality report saved to: {report_file}")
    
    # Save master data
    data_dir = Path(base_path) / "data"
    loader.save_master_data(str(data_dir))
    
    print("\n✓ Data loading complete!")
    print(f"  - Loaded {len(master_data)} tables")
    print(f"  - Master data saved to: {data_dir}")
    

if __name__ == "__main__":
    main()
