"""
Data Cleaning Module for SEC Form D Filings
Handles data cleaning, standardization, and creation of derived fields
"""

import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
import logging
import re

try:
    from .config import (
        INDUSTRY_SECTOR_MAPPING,
        SIC_SECTOR_MAPPING,
        STATE_TO_REGION,
        DEAL_SIZE_BUCKETS,
        INDEFINITE_VALUES,
        FILING_DATE_FORMAT
    )
except ImportError:
    # Allow running as standalone script
    from config import (
        INDUSTRY_SECTOR_MAPPING,
        SIC_SECTOR_MAPPING,
        STATE_TO_REGION,
        DEAL_SIZE_BUCKETS,
        INDEFINITE_VALUES,
        FILING_DATE_FORMAT
    )

logger = logging.getLogger(__name__)


class FormDDataCleaner:
    """
    Cleans and transforms SEC Form D data
    """
    
    def __init__(self, master_data: Dict[str, pd.DataFrame]):
        """
        Initialize the data cleaner
        
        Args:
            master_data: Dictionary of master dataframes from data_loader
        """
        self.master_data = master_data
        self.cleaned_data: Dict[str, pd.DataFrame] = {}
        
    def clean_all_tables(self) -> Dict[str, pd.DataFrame]:
        """
        Clean all tables in the master dataset
        
        Returns:
            Dictionary of cleaned dataframes
        """
        logger.info("=" * 70)
        logger.info("Starting Data Cleaning Process")
        logger.info("=" * 70)
        
        # Clean each table
        self.cleaned_data['submissions'] = self._clean_submissions(
            self.master_data['submissions'].copy()
        )
        self.cleaned_data['issuers'] = self._clean_issuers(
            self.master_data['issuers'].copy()
        )
        self.cleaned_data['offerings'] = self._clean_offerings(
            self.master_data['offerings'].copy()
        )
        self.cleaned_data['recipients'] = self.master_data['recipients'].copy()
        self.cleaned_data['related_persons'] = self.master_data['related_persons'].copy()
        self.cleaned_data['signatures'] = self.master_data['signatures'].copy()
        
        # Create joined analytical dataset
        logger.info("\nCreating master analytical dataset...")
        self.cleaned_data['analytical'] = self._create_analytical_dataset()
        
        logger.info("\n✓ Data cleaning complete!")
        return self.cleaned_data
    
    def _clean_submissions(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean submissions table
        """
        logger.info("\nCleaning SUBMISSIONS table...")
        
        # Parse filing date - use flexible format to handle multiple date formats
        # across different years (e.g., '2008-01-02 06:01:00', '31-DEC-2025', etc.)
        df['filing_date'] = pd.to_datetime(df['FILING_DATE'], errors='coerce', format='mixed', dayfirst=False)
        
        # Extract year and month from parsed dates
        df['filing_year'] = df['filing_date'].dt.year
        df['filing_month'] = df['filing_date'].dt.month
        df['filing_quarter'] = df['filing_date'].dt.quarter
        
        # Fallback: use data_year/data_quarter metadata when filing_date couldn't be parsed
        mask_no_date = df['filing_date'].isna()
        if mask_no_date.any():
            df.loc[mask_no_date, 'filing_year'] = df.loc[mask_no_date, 'data_year']
            df.loc[mask_no_date, 'filing_quarter'] = df.loc[mask_no_date, 'data_quarter']
            # Approximate filing_month from quarter midpoint
            df.loc[mask_no_date, 'filing_month'] = (df.loc[mask_no_date, 'data_quarter'] - 1) * 3 + 2
            # Create approximate filing_date from year/quarter
            df.loc[mask_no_date, 'filing_date'] = pd.to_datetime(
                df.loc[mask_no_date, 'filing_year'].astype(int).astype(str) + '-' +
                df.loc[mask_no_date, 'filing_month'].astype(int).astype(str) + '-15',
                errors='coerce'
            )
            logger.info(f"  Filled {mask_no_date.sum():,} missing dates using data_year/data_quarter")
        
        # Clean SIC code
        df['sic_code'] = df['SIC_CODE'].fillna('').str.strip()
        
        # Amendment flag
        df['is_amendment'] = df['SUBMISSIONTYPE'].str.contains('D/A', case=False, na=False)
        
        logger.info(f"  Parsed {df['filing_date'].notna().sum():,} filing dates")
        logger.info(f"  Identified {df['is_amendment'].sum():,} amendments")
        
        return df
    
    def _clean_issuers(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean issuers table
        """
        logger.info("\nCleaning ISSUERS table...")
        
        # Standardize state codes
        df['state'] = df['STATEORCOUNTRY'].str.strip().str.upper()
        df['is_us'] = df['state'].isin(STATE_TO_REGION.keys())
        
        # Map to regions
        df['region'] = df['state'].map(STATE_TO_REGION)
        df['region'] = df['region'].fillna('International')
        
        # Clean entity name
        df['entity_name_clean'] = df['ENTITYNAME'].str.strip()
        
        # Parse incorporation year
        df['incorporation_year'] = pd.to_numeric(
            df['YEAROFINC_VALUE_ENTERED'], 
            errors='coerce'
        )
        
        # Entity type standardization
        df['entity_type_clean'] = df['ENTITYTYPE'].str.strip()
        df['is_llc'] = df['entity_type_clean'].str.contains('LLC', case=False, na=False)
        df['is_corporation'] = df['entity_type_clean'].str.contains('Corporation', case=False, na=False)
        df['is_partnership'] = df['entity_type_clean'].str.contains('Partnership', case=False, na=False)
        
        logger.info(f"  Mapped {df['region'].notna().sum():,} entities to regions")
        logger.info(f"  US entities: {df['is_us'].sum():,}")
        logger.info(f"  International entities: {(~df['is_us']).sum():,}")
        
        return df
    
    def _clean_offerings(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean offerings table (most important for analysis)
        """
        logger.info("\nCleaning OFFERINGS table...")
        
        # --- Industry/Sector Mapping ---
        df['industry_raw'] = df['INDUSTRYGROUPTYPE'].fillna('Other')
        df['sector'] = df['industry_raw'].map(INDUSTRY_SECTOR_MAPPING)
        df['sector'] = df['sector'].fillna('Other')
        
        # Try to enhance with SIC code mapping
        sic_df = self.master_data['submissions'][['ACCESSIONNUMBER', 'SIC_CODE']]
        df = df.merge(sic_df, on='ACCESSIONNUMBER', how='left')
        
        # Update sector using SIC code where sector is 'Other' and we have SIC
        mask = (df['sector'] == 'Other') & (df['SIC_CODE'].notna())
        df.loc[mask, 'sector'] = df.loc[mask, 'SIC_CODE'].map(SIC_SECTOR_MAPPING)
        df['sector'] = df['sector'].fillna('Other')
        
        # --- Investment Fund Classification ---
        df['is_fund'] = df['INDUSTRYGROUPTYPE'] == 'Pooled Investment Fund'
        df['fund_type'] = df['INVESTMENTFUNDTYPE'].fillna('N/A')
        
        # --- Offering Amounts ---
        df['total_offering_amount'] = self._parse_amount(df['TOTALOFFERINGAMOUNT'])
        df['total_amount_sold'] = self._parse_amount_numeric(df['TOTALAMOUNTSOLD'])
        df['total_remaining'] = self._parse_amount(df['TOTALREMAINING'])
        
        # Calculate fundraising progress
        df['fundraising_pct'] = np.where(
            (df['total_offering_amount'] > 0) & (df['total_offering_amount'] != np.inf),
            (df['total_amount_sold'] / df['total_offering_amount']) * 100,
            np.nan
        )
        
        # --- Deal Size Categories ---
        df['deal_size_category'] = df['total_offering_amount'].apply(self._categorize_deal_size)
        
        # --- Security Types ---
        df['is_equity'] = df['ISEQUITYTYPE'] == 'true'
        df['is_debt'] = df['ISDEBTTYPE'] == 'true'
        df['is_pooled_fund_interest'] = df['ISPOOLEDINVESTMENTFUNDTYPE'] == 'true'
        
        # --- Investor Information ---
        df['total_investors'] = pd.to_numeric(df['TOTALNUMBERALREADYINVESTED'], errors='coerce').fillna(0)
        df['has_non_accredited'] = df['HASNONACCREDITEDINVESTORS'] == 'true'
        df['num_non_accredited'] = pd.to_numeric(df['NUMBERNONACCREDITEDINVESTORS'], errors='coerce').fillna(0)
        
        # Investor diversity score (simple metric)
        df['investor_diversity'] = np.where(
            df['total_investors'] > 0,
            np.minimum(df['total_investors'] / 10, 10),  # Cap at 10
            0
        )
        
        # --- Sales Compensation ---
        df['sales_commission'] = pd.to_numeric(df['SALESCOMM_DOLLARAMOUNT'], errors='coerce').fillna(0)
        df['finders_fee'] = pd.to_numeric(df['FINDERSFEE_DOLLARAMOUNT'], errors='coerce').fillna(0)
        df['total_sales_comp'] = df['sales_commission'] + df['finders_fee']
        
        # Has professional placement (signal of institutional quality)
        df['has_placement_agent'] = df['total_sales_comp'] > 0
        
        # --- Amendment tracking ---
        df['is_amendment'] = df['ISAMENDMENT'] == 'true'
        df['previous_accession'] = df['PREVIOUSACCESSIONNUMBER'].fillna('')
        
        # --- Sale date parsing ---
        df['sale_date'] = pd.to_datetime(df['SALE_DATE'], errors='coerce')
        df['sale_yet_to_occur'] = df['YETTOOCCUR'] == 'true'
        
        # --- Offering duration ---
        df['offering_duration_long'] = df['MORETHANONEYEAR'] == 'true'
        
        # --- Exemptions ---
        df['exemptions'] = df['FEDERALEXEMPTIONS_ITEMS_LIST'].fillna('')
        df['has_506b'] = df['exemptions'].str.contains('06b', case=False, na=False)
        df['has_506c'] = df['exemptions'].str.contains('06c', case=False, na=False)
        df['has_reg_d'] = df['has_506b'] | df['has_506c']
        
        logger.info(f"  Mapped {len(df)} offerings to sectors")
        logger.info(f"  Sector distribution:")
        for sector, count in df['sector'].value_counts().head(10).items():
            logger.info(f"    {sector}: {count:,}")
        
        logger.info(f"  Deal size categories:")
        for cat, count in df['deal_size_category'].value_counts().items():
            logger.info(f"    {cat}: {count:,}")
        
        logger.info(f"  Investment funds: {df['is_fund'].sum():,}")
        logger.info(f"  Operating companies: {(~df['is_fund']).sum():,}")
        
        return df
    
    def _parse_amount(self, series: pd.Series) -> pd.Series:
        """
        Parse amount fields that may contain 'Indefinite' or numeric values
        'Indefinite' is converted to np.inf for filtering purposes
        """
        def parse_value(val):
            if pd.isna(val):
                return np.nan
            if isinstance(val, (int, float)):
                return float(val)
            val_str = str(val).strip().upper()
            if val_str in INDEFINITE_VALUES:
                return np.inf
            try:
                # Remove commas and convert to float
                return float(val_str.replace(',', ''))
            except (ValueError, AttributeError):
                return np.nan
        
        return series.apply(parse_value)
    
    def _parse_amount_numeric(self, series: pd.Series) -> pd.Series:
        """
        Parse amount fields as pure numeric (NaN for indefinite)
        """
        def parse_value(val):
            if pd.isna(val):
                return np.nan
            if isinstance(val, (int, float)):
                return float(val)
            val_str = str(val).strip().upper()
            if val_str in INDEFINITE_VALUES:
                return np.nan
            try:
                return float(val_str.replace(',', ''))
            except (ValueError, AttributeError):
                return np.nan
        
        return series.apply(parse_value)
    
    def _categorize_deal_size(self, amount: float) -> str:
        """
        Categorize deal size into buckets
        """
        if pd.isna(amount) or amount == np.inf:
            return 'Unknown'
        
        for category, lower, upper in DEAL_SIZE_BUCKETS:
            if lower <= amount < upper:
                return category
        
        return 'Unknown'
    
    def _create_analytical_dataset(self) -> pd.DataFrame:
        """
        Create joined analytical dataset with all relevant fields
        """
        # Start with offerings (one row per offering)
        df = self.cleaned_data['offerings'].copy()
        
        # Join with issuers (get company info)
        issuers = self.cleaned_data['issuers'][
            self.cleaned_data['issuers']['IS_PRIMARYISSUER_FLAG'] == 'YES'
        ][[
            'ACCESSIONNUMBER', 'entity_name_clean', 'state', 'region', 'is_us',
            'CITY', 'ZIPCODE', 'entity_type_clean', 'incorporation_year',
            'is_llc', 'is_corporation', 'is_partnership'
        ]]
        
        df = df.merge(issuers, on='ACCESSIONNUMBER', how='left')
        
        # Join with submissions (get filing metadata)
        submissions = self.cleaned_data['submissions'][[
            'ACCESSIONNUMBER', 'filing_date', 'filing_year', 'filing_month',
            'filing_quarter', 'sic_code', 'data_period'
        ]]
        
        df = df.merge(submissions, on='ACCESSIONNUMBER', how='left')
        
        # Calculate offering age (days since filing)
        df['offering_age_days'] = (pd.Timestamp.now() - df['filing_date']).dt.days
        
        # Count related persons per offering (signal of team size/quality)
        related_counts = self.master_data['related_persons'].groupby('ACCESSIONNUMBER').size()
        df['num_related_persons'] = df['ACCESSIONNUMBER'].map(related_counts).fillna(0).astype(int)
        
        # Check if offering has recipients (placement agents)
        recipients_present = self.master_data['recipients']['ACCESSIONNUMBER'].unique()
        df['has_recipients'] = df['ACCESSIONNUMBER'].isin(recipients_present)
        
        # Identify follow-on offerings (has previous accession number or multiple filings by same issuer)
        # Count filings per entity
        entity_filing_counts = df.groupby('entity_name_clean')['ACCESSIONNUMBER'].transform('count')
        df['entity_filing_count'] = entity_filing_counts
        df['is_follow_on'] = (df['is_amendment']) | (df['entity_filing_count'] > 1)
        
        # Active fundraising (has remaining amount to raise)
        df['is_active'] = (df['total_remaining'] > 0) & (df['total_remaining'] != np.inf)
        
        # Recent filing (within last 18 months)
        df['is_recent'] = df['offering_age_days'] <= 540  # 18 months
        
        logger.info(f"  Created analytical dataset with {len(df):,} rows and {len(df.columns)} columns")
        logger.info(f"  Date range: {df['filing_date'].min()} to {df['filing_date'].max()}")
        
        return df
    
    def save_cleaned_data(self, output_dir: str):
        """
        Save cleaned data to files
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"\nSaving cleaned data to {output_path}...")
        
        for table_type, df in self.cleaned_data.items():
            file_path = output_path / f"cleaned_{table_type}.csv"
            df.to_csv(file_path, index=False)
            logger.info(f"  Saved {table_type}: {len(df):,} rows")


def main():
    """
    Test the data cleaner
    """
    from .data_loader import FormDDataLoader
    
    base_path = "/Users/bhumikamarmat/sec filings"
    
    # Load data
    loader = FormDDataLoader(base_path)
    master_data = loader.load_all_data()
    
    # Clean data
    cleaner = FormDDataCleaner(master_data)
    cleaned_data = cleaner.clean_all_tables()
    
    # Save cleaned data
    data_dir = Path(base_path) / "data"
    cleaner.save_cleaned_data(str(data_dir))
    
    # Show analytical dataset sample
    print("\n" + "=" * 70)
    print("ANALYTICAL DATASET PREVIEW")
    print("=" * 70)
    print(cleaned_data['analytical'][[ 'entity_name_clean', 'sector', 'state', 'region',
        'total_offering_amount', 'total_amount_sold', 'deal_size_category',
        'filing_date', 'is_fund', 'is_follow_on'
    ]].head(20))
    
    print("\n✓ Data cleaning complete!")


if __name__ == "__main__":
    main()
