"""
AI/SaaS Target Company Generator for Z5 Capital
Identifies and scores AI and SaaS companies from Form D data
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ============================================================
# Z5 CAPITAL AI/SaaS INVESTMENT THESIS CONFIG
# ============================================================

# AI/ML keywords to match in entity names (case-insensitive)
AI_KEYWORDS = [
    'ARTIFICIAL INTELLIGENCE', 'MACHINE LEARNING', 'DEEP LEARNING',
    'NEURAL NETWORK', 'COMPUTER VISION', 'NATURAL LANGUAGE',
    'GENERATIVE AI', 'GENAI', 'GPT', 'LLM',
    'COGNITIVE', 'PREDICTIVE ANALYTICS', 'AUTONOMOUS',
    'REINFORCEMENT LEARNING', 'CONVERSATIONAL AI',
]

# SaaS/Software keywords to match in entity names
SAAS_KEYWORDS = [
    'SOFTWARE', 'SAAS', 'CLOUD', ' PLATFORM',
    'ANALYTICS', 'DATA SCIENCE', 'AUTOMATION',
    'CYBERSECURITY', 'CYBER SECURITY', 'INFOSEC',
    'ROBOTIC', 'RPA', 'DEVOPS', 'API ',
    'FINTECH', 'PROPTECH', 'EDTECH', 'HEALTHTECH',
    'MEDTECH', 'MARTECH', 'ADTECH', 'REGTECH', 'LEGALTECH',
    'INSURTECH', 'AGTECH', 'FOODTECH', 'GOVTECH',
    'DIGITAL HEALTH', 'TELEHEALTH', 'TELEMEDICINE',
]

# SEC Industry Group Types that signal tech/software companies
TECH_INDUSTRY_TYPES = ['Other Technology', 'Computers', 'Business Services']

# Target geographies (innovation hubs)
TARGET_STATES = ['CA', 'NY', 'MA', 'TX', 'WA', 'IL', 'FL', 'CO', 'UT', 'GA', 'NC', 'VA']

# Ideal deal size range for Z5 thesis
IDEAL_MIN_SIZE = 1_000_000    # $1M
IDEAL_MAX_SIZE = 50_000_000   # $50M

# AI sub-category detection for richer classification
AI_SUBCATEGORY_PATTERNS = {
    'Computer Vision': ['COMPUTER VISION', 'IMAGE RECOGNITION', 'OBJECT DETECTION', 'VIDEO ANALYTICS'],
    'NLP / LLM': ['NATURAL LANGUAGE', 'NLP', 'LLM', 'GPT', 'LANGUAGE MODEL', 'CONVERSATIONAL AI', 'CHATBOT'],
    'Generative AI': ['GENERATIVE AI', 'GENAI', 'GEN AI', 'DIFFUSION', 'FOUNDATION MODEL'],
    'ML Platform': ['MACHINE LEARNING', 'ML PLATFORM', 'MLOPS', 'MODEL TRAINING', 'DEEP LEARNING'],
    'Autonomous Systems': ['AUTONOMOUS', 'SELF-DRIVING', 'SELF DRIVING', 'DRONE', 'ROBOTIC'],
    'Predictive Analytics': ['PREDICTIVE', 'FORECASTING', 'ANALYTICS'],
    'Cybersecurity AI': ['CYBERSECURITY', 'CYBER SECURITY', 'INFOSEC', 'THREAT DETECTION'],
    'Healthcare AI': ['DIGITAL HEALTH', 'HEALTHTECH', 'MEDTECH', 'TELEHEALTH', 'CLINICAL AI'],
    'Fintech AI': ['FINTECH', 'REGTECH', 'INSURTECH', 'WEALTHTECH'],
    'Enterprise SaaS': ['SOFTWARE', 'SAAS', 'CLOUD', 'PLATFORM', 'ENTERPRISE'],
    'Data Infrastructure': ['DATA SCIENCE', 'DATA ENGINEERING', 'DATA PIPELINE', 'DATABASE', 'DATA LAKE'],
    'DevTools': ['DEVOPS', 'API ', 'DEVELOPER', 'LOW CODE', 'NO CODE'],
}


class AISaaSTargetGenerator:
    """
    Identifies, classifies, and scores AI/SaaS companies from Form D filings
    """
    
    def __init__(self, analytical_df: pd.DataFrame):
        self.df = analytical_df.copy()
        self.df['_name_upper'] = self.df['entity_name_clean'].fillna('').str.upper()
        
    def identify_ai_saas(self) -> pd.DataFrame:
        """
        Filter dataset to AI/SaaS companies using multi-signal approach:
        1. SEC Industry Group Type (Technology, Computers, Business Services)
        2. AI keywords in entity name
        3. SaaS keywords in entity name
        """
        name = self.df['_name_upper']
        
        # Signal 1: SEC Industry classification
        tech_industry = self.df['INDUSTRYGROUPTYPE'].isin(TECH_INDUSTRY_TYPES)
        
        # Signal 2: AI keywords in name
        ai_mask = pd.Series(False, index=self.df.index)
        for kw in AI_KEYWORDS:
            ai_mask |= name.str.contains(kw, na=False)
        # Standalone "AI" with word boundary (avoid CHAIR, AFFAIR, CERTAIN, etc.)
        ai_standalone = name.str.contains(r'\bAI\b', regex=True, na=False)
        false_positives = name.str.contains(
            'CHAIR|ACQUI|DOMAIN|CERTAIN|CONTAIN|REPAIR|AFFAIR|TRAIL|NAIF|CAPITAL|FUND|VENTURE|PARTNER',
            na=False
        )
        ai_mask |= (ai_standalone & ~false_positives)
        
        # Signal 3: SaaS keywords in name
        saas_mask = pd.Series(False, index=self.df.index)
        for kw in SAAS_KEYWORDS:
            saas_mask |= name.str.contains(kw, na=False)
        
        # Exclude investment funds
        is_fund = self.df['is_fund'].astype(str).str.lower().isin(['true', '1', '1.0'])
        
        # Combined: any signal and not a fund
        ai_saas = (tech_industry | ai_mask | saas_mask) & ~is_fund
        
        result = self.df[ai_saas].copy()
        
        # Tag the identification source
        result['ai_signal'] = ai_mask[ai_saas].values
        result['saas_signal'] = saas_mask[ai_saas].values
        result['tech_industry_signal'] = tech_industry[ai_saas].values
        
        # Classify sub-category
        result['ai_subcategory'] = result['_name_upper'].apply(self._classify_subcategory)
        
        logger.info(f"Identified {len(result):,} AI/SaaS filings from {result['entity_name_clean'].nunique():,} unique entities")
        logger.info(f"  AI keyword match: {result['ai_signal'].sum():,}")
        logger.info(f"  SaaS keyword match: {result['saas_signal'].sum():,}")
        logger.info(f"  Tech industry type: {result['tech_industry_signal'].sum():,}")
        
        return result
    
    def _classify_subcategory(self, name: str) -> str:
        """Classify AI/SaaS subcategory from entity name"""
        for category, patterns in AI_SUBCATEGORY_PATTERNS.items():
            for pat in patterns:
                if pat in name:
                    return category
        return 'General Tech/SaaS'
    
    def generate_targets(self, min_score: int = 15, top_n: int = 200) -> pd.DataFrame:
        """
        Generate scored AI/SaaS target list for Z5 Capital
        """
        logger.info("=" * 70)
        logger.info("Z5 CAPITAL — AI/SaaS TARGET COMPANY GENERATOR")
        logger.info("=" * 70)
        
        # Step 1: Identify AI/SaaS companies
        ai_saas = self.identify_ai_saas()
        
        # Step 2: Filter to recent filings (last 2 years by data_year)
        recent_years = ai_saas['data_year'].astype(float) >= 2024
        targets = ai_saas[recent_years].copy()
        
        logger.info(f"\nRecent AI/SaaS pool (2024-2025): {len(targets):,} filings, {targets['entity_name_clean'].nunique():,} unique entities")
        
        if len(targets) == 0:
            # Fallback to last 3 years
            recent_years = ai_saas['data_year'].astype(float) >= 2023
            targets = ai_saas[recent_years].copy()
            logger.info(f"Expanded to 2023+: {len(targets):,} filings")
        
        # Step 3: Score each filing
        targets['ai_score'] = targets.apply(self._score_ai_fit, axis=1)
        targets['size_score'] = targets['total_offering_amount'].apply(self._score_deal_size)
        targets['geo_score'] = targets['state'].apply(self._score_geography)
        targets['momentum_score'] = targets.apply(self._score_momentum, axis=1)
        targets['quality_score'] = targets.apply(self._score_quality, axis=1)
        
        # Weighted total
        targets['total_score'] = (
            targets['ai_score'] * 0.30 +      # AI/SaaS fit is most important
            targets['momentum_score'] * 0.25 +
            targets['size_score'] * 0.20 +
            targets['geo_score'] * 0.10 +
            targets['quality_score'] * 0.15
        )
        
        # Filter and deduplicate (keep best filing per entity)
        targets = targets.sort_values('total_score', ascending=False)
        targets = targets.drop_duplicates(subset='entity_name_clean', keep='first')
        targets = targets[targets['total_score'] >= min_score]
        
        # Select output columns
        output_cols = [
            'entity_name_clean', 'ai_subcategory', 'INDUSTRYGROUPTYPE',
            'state', 'region', 'CITY',
            'total_offering_amount', 'total_amount_sold', 'deal_size_category',
            'data_period', 'total_investors', 'has_placement_agent',
            'is_follow_on', 'num_related_persons',
            'total_score', 'ai_score', 'size_score', 'geo_score',
            'momentum_score', 'quality_score',
            'ai_signal', 'saas_signal', 'tech_industry_signal',
            'ACCESSIONNUMBER'
        ]
        
        available_cols = [c for c in output_cols if c in targets.columns]
        result = targets[available_cols].head(top_n).copy()
        
        # Format amounts
        result['offering_amount_m'] = result['total_offering_amount'] / 1e6
        result['amount_sold_m'] = result['total_amount_sold'] / 1e6
        
        logger.info(f"\n✓ Generated {len(result)} AI/SaaS targets")
        if len(result) > 0:
            logger.info(f"  Score range: {result['total_score'].min():.1f} - {result['total_score'].max():.1f}")
            logger.info(f"  Avg score: {result['total_score'].mean():.1f}")
            
            logger.info(f"\nAI/SaaS Sub-categories:")
            for cat, count in result['ai_subcategory'].value_counts().head(10).items():
                logger.info(f"  {cat}: {count}")
            
            logger.info(f"\nTop States:")
            for state, count in result['state'].value_counts().head(8).items():
                logger.info(f"  {state}: {count}")
            
            logger.info(f"\nDeal Size Distribution:")
            for cat, count in result['deal_size_category'].value_counts().items():
                logger.info(f"  {cat}: {count}")
        
        return result
    
    def _score_ai_fit(self, row) -> float:
        """Score based on AI/SaaS alignment (0-30)"""
        score = 0.0
        
        # Direct AI keyword match is strongest signal
        if row.get('ai_signal', False):
            score += 20.0
        
        # SaaS keyword match
        if row.get('saas_signal', False):
            score += 15.0
        
        # Tech industry classification
        if row.get('tech_industry_signal', False):
            score += 10.0
        
        # Sub-category bonus for hot areas
        hot_categories = ['NLP / LLM', 'Generative AI', 'Computer Vision', 'ML Platform', 'Cybersecurity AI']
        if row.get('ai_subcategory', '') in hot_categories:
            score += 5.0
        
        return min(score, 30.0)
    
    def _score_deal_size(self, amount: float) -> float:
        """Score based on deal size fit (0-20)"""
        if pd.isna(amount) or amount == np.inf:
            return 0.0
        
        if IDEAL_MIN_SIZE <= amount <= IDEAL_MAX_SIZE:
            return 20.0
        elif amount < IDEAL_MIN_SIZE:
            ratio = amount / IDEAL_MIN_SIZE
            return max(5.0, 15.0 * ratio)
        else:
            if amount <= IDEAL_MAX_SIZE * 2:
                return 12.0
            else:
                return 5.0
    
    def _score_geography(self, state: str) -> float:
        """Score based on geography (0-10)"""
        if pd.isna(state):
            return 0.0
        if state in TARGET_STATES:
            return 10.0
        elif state in ['DE', 'MD', 'PA', 'NJ', 'OR', 'AZ', 'NV', 'MN']:
            return 7.0
        else:
            return 3.0
    
    def _score_momentum(self, row) -> float:
        """Score based on momentum indicators (0-25)"""
        score = 0.0
        
        if row.get('is_follow_on', False):
            score += 10.0
        
        sold = row.get('total_amount_sold', 0)
        if pd.notna(sold) and sold > 1_000_000:
            score += 7.0
        elif pd.notna(sold) and sold > 100_000:
            score += 3.0
        
        investors = row.get('total_investors', 0)
        if pd.notna(investors) and investors >= 10:
            score += 8.0
        elif pd.notna(investors) and investors >= 3:
            score += 5.0
        elif pd.notna(investors) and investors >= 1:
            score += 2.0
        
        return min(score, 25.0)
    
    def _score_quality(self, row) -> float:
        """Score based on quality signals (0-15)"""
        score = 0.0
        
        if row.get('has_placement_agent', False) or row.get('has_recipients', False):
            score += 6.0
        
        rp = row.get('num_related_persons', 0)
        if pd.notna(rp) and rp >= 5:
            score += 5.0
        elif pd.notna(rp) and rp >= 2:
            score += 3.0
        
        # Equity offering preferred
        if row.get('is_equity', False):
            score += 4.0
        
        return min(score, 15.0)

    def generate_full_list(self) -> pd.DataFrame:
        """
        Generate complete list of ALL AI/SaaS companies across all years
        (not just recent), deduplicated by entity name, with latest filing
        """
        logger.info("=" * 70)
        logger.info("GENERATING FULL AI/SaaS COMPANY UNIVERSE")
        logger.info("=" * 70)
        
        ai_saas = self.identify_ai_saas()
        
        # Take latest filing per entity
        ai_saas = ai_saas.sort_values('data_year', ascending=False)
        unique_entities = ai_saas.drop_duplicates(subset='entity_name_clean', keep='first')
        
        output_cols = [
            'entity_name_clean', 'ai_subcategory', 'INDUSTRYGROUPTYPE',
            'state', 'region', 'CITY',
            'total_offering_amount', 'total_amount_sold', 'deal_size_category',
            'data_period', 'data_year', 'total_investors',
            'ai_signal', 'saas_signal', 'tech_industry_signal',
        ]
        
        available_cols = [c for c in output_cols if c in unique_entities.columns]
        result = unique_entities[available_cols].copy()
        result['offering_amount_m'] = result['total_offering_amount'] / 1e6
        
        logger.info(f"Full AI/SaaS universe: {len(result):,} unique entities")
        
        return result


def main():
    """
    Generate AI/SaaS target company list for Z5 Capital
    """
    base_path = Path("/Users/bhumikamarmat/sec filings")
    data_path = base_path / "data" / "cleaned_analytical.csv"
    
    print("Loading analytical dataset...")
    df = pd.read_csv(data_path, low_memory=False)
    df['filing_date'] = pd.to_datetime(df['filing_date'], errors='coerce')
    df['sale_date'] = pd.to_datetime(df['sale_date'], errors='coerce')
    
    print(f"Loaded {len(df):,} offerings\n")
    
    # Generate AI/SaaS targets
    generator = AISaaSTargetGenerator(df)
    
    # 1. Scored target list (recent, high-quality)
    targets = generator.generate_targets(min_score=15, top_n=200)
    
    target_path = base_path / "reports" / "target_companies.csv"
    targets.to_csv(target_path, index=False)
    print(f"\n✓ Saved scored target list ({len(targets)} companies) to: {target_path}")
    
    # 2. Full AI/SaaS universe (all years)
    full_list = generator.generate_full_list()
    
    full_path = base_path / "reports" / "ai_saas_universe.csv"
    full_list.to_csv(full_path, index=False)
    print(f"✓ Saved full AI/SaaS universe ({len(full_list):,} entities) to: {full_path}")
    
    # Show top 30 targets
    print("\n" + "=" * 120)
    print("Z5 CAPITAL — TOP 30 AI/SaaS TARGET COMPANIES")
    print("=" * 120)
    
    display_cols = ['entity_name_clean', 'ai_subcategory', 'state', 'offering_amount_m',
                    'total_investors', 'total_score']
    
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 120)
    pd.set_option('display.max_colwidth', 45)
    
    print(targets[display_cols].head(30).to_string(index=False))
    
    # Summary by sub-category
    print("\n" + "=" * 120)
    print("AI/SaaS UNIVERSE BY SUB-CATEGORY")
    print("=" * 120)
    for cat, count in full_list['ai_subcategory'].value_counts().items():
        print(f"  {cat:30s}: {count:>6,}")
    
    print("\n" + "=" * 120)
    print(f"TOTAL UNIQUE AI/SaaS ENTITIES: {len(full_list):,}")
    print(f"SCORED TARGETS (2024-2025): {len(targets)}")
    print("=" * 120)


if __name__ == "__main__":
    main()
