"""
Target Company Generator
Creates scored list of investment opportunities from Form D data
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Scoring configuration
TARGET_SECTORS = ['Biotech', 'Pharma', 'Energy', 'Fintech', 'Healthcare IT', 'Enterprise Software', 
                  'Cybersecurity', 'Data & Analytics', 'AgTech']
TARGET_STATES = ['CA', 'NY', 'MA', 'TX', 'WA', 'IL', 'FL', 'CO', 'UT', 'GA', 'NC']
IDEAL_MIN_SIZE = 5_000_000
IDEAL_MAX_SIZE = 25_000_000


class TargetGenerator:
    """
    Generates and scores investment opportunities
    """
    
    def __init__(self, analytical_df: pd.DataFrame):
        """
        Initialize with analytical dataset
        """
        self.df = analytical_df.copy()
        
    def generate_targets(self, min_score: int = 20, top_n: int = 100) -> pd.DataFrame:
        """
        Generate scored target list
        
        Args:
            min_score: Minimum score threshold (0-100)
            top_n: Number of top targets to return
        
        Returns:
            DataFrame of scored targets
        """
        logger.info("=" * 70)
        logger.info("GENERATING TARGET COMPANY LIST")
        logger.info("=" * 70)
        
        # Filter to operating companies only
        targets = self.df[~self.df['is_fund']].copy()
        
        # Filter to recent filings (last 18 months)
        targets = targets[targets['is_recent'] == True]
        
        logger.info(f"\nStarting pool: {len(targets):,} recent operating company offerings")
        
        # Calculate scores
        targets['sector_score'] = targets['sector'].apply(self._score_sector)
        targets['size_score'] = targets['total_offering_amount'].apply(self._score_deal_size)
        targets['geo_score'] = targets['state'].apply(self._score_geography)
        targets['momentum_score'] = targets.apply(self._score_momentum, axis=1)
        targets['quality_score'] = targets.apply(self._score_quality, axis=1)
        
        # Calculate total score (weighted)
        weights = {
            'sector': 0.25,
            'size': 0.20,
            'geo': 0.15,
            'momentum': 0.25,
            'quality': 0.15
        }
        
        targets['total_score'] = (
            targets['sector_score'] * weights['sector'] +
            targets['size_score'] * weights['size'] +
            targets['geo_score'] * weights['geo'] +
            targets['momentum_score'] * weights['momentum'] +
            targets['quality_score'] * weights['quality']
        )
        
        # Filter by minimum score
        targets = targets[targets['total_score'] >= min_score]
        
        logger.info(f"After scoring filter (>={min_score}): {len(targets):,} companies")
        
        # Sort by score
        targets = targets.sort_values('total_score', ascending=False)
        
        # Select output columns
        output_cols = [
            'entity_name_clean', 'sector', 'state', 'region', 'CITY',
            'total_offering_amount', 'total_amount_sold', 'deal_size_category',
            'filing_date', 'total_investors', 'has_placement_agent',
            'is_follow_on', 'num_related_persons', 'offering_age_days',
            'total_score', 'sector_score', 'size_score', 'geo_score',
            'momentum_score', 'quality_score', 'ACCESSIONNUMBER'
        ]
        
        result = targets[output_cols].head(top_n).copy()
        
        # Format amounts
        result['offering_amount_m'] = result['total_offering_amount'] / 1e6
        result['amount_sold_m'] = result['total_amount_sold'] / 1e6
        
        logger.info(f"\n✓ Generated top {len(result)} targets")
        logger.info(f"  Score range: {result['total_score'].min():.1f} - {result['total_score'].max():.1f}")
        logger.info(f"  Avg score: {result['total_score'].mean():.1f}")
        
        # Summary stats
        logger.info(f"\nTop Targets by Sector:")
        for sector, count in result['sector'].value_counts().head(10).items():
            logger.info(f"  {sector}: {count}")
        
        logger.info(f"\nTop Targets by State:")
        for state, count in result['state'].value_counts().head(5).items():
            logger.info(f"  {state}: {count}")
        
        return result
    
    def _score_sector(self, sector: str) -> float:
        """Score based on sector alignment (0-25)"""
        if sector in TARGET_SECTORS:
            return 25.0
        elif sector in ['Healthcare', 'Insurance', 'Real Estate', 'Consumer']:
            return 15.0
        elif sector == 'Other':
            return 5.0
        else:
            return 10.0
    
    def _score_deal_size(self, amount: float) -> float:
        """Score based on deal size fit (0-20)"""
        if pd.isna(amount) or amount == np.inf:
            return 0.0
        
        if IDEAL_MIN_SIZE <= amount <= IDEAL_MAX_SIZE:
            return 20.0
        elif amount < IDEAL_MIN_SIZE:
            # Below ideal - score decreases with distance
            ratio = amount / IDEAL_MIN_SIZE
            return 15.0 * ratio
        else:
            # Above ideal - moderate penalty
            if amount <= IDEAL_MAX_SIZE * 2:
                return 12.0
            else:
                return 5.0
    
    def _score_geography(self, state: str) -> float:
        """Score based on geography (0-15)"""
        if pd.isna(state):
            return 0.0
        
        if state in TARGET_STATES:
            return 15.0
        elif state in ['DE', 'MD', 'VA', 'NC', 'SC', 'TN', 'OR', 'AZ', 'NV']:
            return 10.0
        else:
            return 5.0
    
    def _score_momentum(self, row) -> float:
        """Score based on momentum indicators (0-25)"""
        score = 0.0
        
        # Follow-on round
        if row['is_follow_on']:
            score += 10.0
        
        # Has raised significant capital
        if row['total_amount_sold'] > 1_000_000:
            score += 7.0
        
        # Multiple investors
        if row['total_investors'] >= 5:
            score += 8.0
        elif row['total_investors'] >= 2:
            score += 4.0
        
        return min(score, 25.0)
    
    def _score_quality(self, row) -> float:
        """Score based on quality signals (0-15)"""
        score = 0.0
        
        # Placement agent involvement
        if row['has_placement_agent'] or row['has_recipients']:
            score += 7.0
        
        # Team size (related persons)
        if row['num_related_persons'] >= 3:
            score += 5.0
        elif row['num_related_persons'] >= 1:
            score += 3.0
        
        # Not too old (within 12 months)
        if row['offering_age_days'] <= 365:
            score += 3.0
        
        return min(score, 15.0)


def main():
    """
    Generate target company list
    """
    base_path = Path("/Users/bhumikamarmat/sec filings")
    data_path = base_path / "data" / "cleaned_analytical.csv"
    
    print("Loading analytical dataset...")
    df = pd.read_csv(data_path, low_memory=False)
    df['filing_date'] = pd.to_datetime(df['filing_date'], errors='coerce')
    df['sale_date'] = pd.to_datetime(df['sale_date'], errors='coerce')
    
    print(f"Loaded {len(df):,} offerings\n")
    
    # Generate targets
    generator = TargetGenerator(df)
    targets = generator.generate_targets(min_score=20, top_n=100)
    
    # Save to file
    output_path = base_path / "reports" / "target_companies.csv"
    targets.to_csv(output_path, index=False)
    
    print(f"\n✓ Saved target list to: {output_path}")
    
    # Show top 20
    print("\n" + "=" * 100)
    print("TOP 20 TARGET COMPANIES")
    print("=" * 100)
    
    display_cols = ['entity_name_clean', 'sector', 'state', 'offering_amount_m', 
                    'total_investors', 'is_follow_on', 'total_score']
    
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 40)
    
    print(targets[display_cols].head(20).to_string(index=False))
    
    print("\n" + "=" * 100)
    print(f"Full list of {len(targets)} targets saved to reports/target_companies.csv")
    print("=" * 100)


if __name__ == "__main__":
    main()
