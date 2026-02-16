"""
Configuration file for SEC Form D analysis
Customize fund thesis parameters, scoring weights, and preferences here
"""

# ============================================================================
# FUND THESIS CONFIGURATION
# ============================================================================

# Target sectors (can customize based on your fund's focus)
TARGET_SECTORS = [
    'Enterprise Software',
    'Artificial Intelligence',
    'Fintech',
    'Healthcare IT',
    'SaaS',
    'Cybersecurity',
    'Data & Analytics'
]

# Target geographies (states)
TARGET_STATES = ['CA', 'NY', 'MA', 'TX', 'WA', 'IL', 'FL', 'CO']

# Target regions
TARGET_REGIONS = ['West Coast', 'Northeast', 'Southwest']

# Deal size preferences (in USD)
MIN_DEAL_SIZE = 1_000_000      # $1M
MAX_DEAL_SIZE = 50_000_000     # $50M
IDEAL_MIN = 5_000_000          # $5M
IDEAL_MAX = 25_000_000         # $25M

# ============================================================================
# SCORING MODEL WEIGHTS (must sum to 100)
# ============================================================================

SCORING_WEIGHTS = {
    'sector_fit': 25,           # Alignment with target sectors
    'deal_size_fit': 20,        # Match to ideal deal size range
    'geographic_fit': 15,       # Location in target states/regions
    'momentum': 25,             # Growth signals (follow-ons, increasing amounts)
    'quality_signals': 15       # Institutional signals, completeness
}

# ============================================================================
# INDUSTRY STANDARDIZATION MAPPING
# ============================================================================

# Map Form D industry types to standardized sectors
INDUSTRY_SECTOR_MAPPING = {
    # Technology
    'Computers': 'Enterprise Software',
    'Computer Software': 'Enterprise Software',
    'Technology': 'Enterprise Software',
    'Internet and Information Services': 'Enterprise Software',
    'Telecommunications': 'Telecommunications',
    'Electronics': 'Hardware',
    
    # Finance
    'Banking and Financial Services': 'Fintech',
    'Insurance': 'Insurtech',
    'Real Estate': 'Real Estate',
    
    # Healthcare
    'Health Care': 'Healthcare',
    'Biotechnology': 'Biotech',
    'Pharmaceuticals': 'Pharma',
    
    # Energy & Resources
    'Energy': 'Energy',
    'Oil and Gas': 'Energy',
    'Mining': 'Mining',
    'Agriculture': 'AgTech',
    
    # Consumer
    'Retailing': 'Consumer',
    'Restaurants': 'Consumer',
    'Consumer Services': 'Consumer',
    
    # Industrial
    'Manufacturing': 'Industrial',
    'Transportation': 'Transportation',
    'Construction': 'Construction',
    
    # Investment Funds
    'Pooled Investment Fund': 'Investment Fund',
    
    # Other
    'Other': 'Other'
}

# SIC code to sector mapping (supplement to industry mapping)
SIC_SECTOR_MAPPING = {
    # Technology (7370-7379, 3570-3579)
    '7370': 'Enterprise Software',
    '7371': 'Enterprise Software',
    '7372': 'Enterprise Software',
    '7373': 'Enterprise Software',
    '7374': 'Data & Analytics',
    '7375': 'Enterprise Software',
    '3571': 'Hardware',
    '3572': 'Hardware',
    '3576': 'Hardware',
    '3577': 'Hardware',
    '3661': 'Telecommunications',
    
    # Finance (6000-6999)
    '6022': 'Fintech',
    '6036': 'Fintech',
    '6211': 'Fintech',
    '6282': 'Fintech',
    '6311': 'Insurtech',
    '6531': 'Real Estate',
    
    # Healthcare (8000-8099, 2830-2836, 3840-3851)
    '8000': 'Healthcare',
    '8011': 'Healthcare',
    '8060': 'Healthcare',
    '8071': 'Healthcare IT',
    '2834': 'Pharma',
    '2836': 'Biotech',
    '3841': 'Healthcare',
    '3845': 'Healthcare',
    
    # Energy (1311, 1381, 4911-4939)
    '1311': 'Energy',
    '1381': 'Energy',
    '4911': 'Energy',
    '4922': 'Energy',
}

# ============================================================================
# GEOGRAPHIC REGION MAPPING
# ============================================================================

STATE_TO_REGION = {
    # West Coast
    'CA': 'West Coast',
    'OR': 'West Coast',
    'WA': 'West Coast',
    
    # Northeast
    'NY': 'Northeast',
    'MA': 'Northeast',
    'CT': 'Northeast',
    'NJ': 'Northeast',
    'PA': 'Northeast',
    'NH': 'Northeast',
    'VT': 'Northeast',
    'RI': 'Northeast',
    'ME': 'Northeast',
    
    # Southeast
    'FL': 'Southeast',
    'GA': 'Southeast',
    'NC': 'Southeast',
    'SC': 'Southeast',
    'VA': 'Southeast',
    'TN': 'Southeast',
    'AL': 'Southeast',
    'MS': 'Southeast',
    'LA': 'Southeast',
    'AR': 'Southeast',
    'KY': 'Southeast',
    'WV': 'Southeast',
    
    # Midwest
    'IL': 'Midwest',
    'OH': 'Midwest',
    'MI': 'Midwest',
    'IN': 'Midwest',
    'WI': 'Midwest',
    'MN': 'Midwest',
    'IA': 'Midwest',
    'MO': 'Midwest',
    'KS': 'Midwest',
    'NE': 'Midwest',
    'SD': 'Midwest',
    'ND': 'Midwest',
    
    # Southwest
    'TX': 'Southwest',
    'AZ': 'Southwest',
    'NM': 'Southwest',
    'OK': 'Southwest',
    
    # Mountain West
    'CO': 'Mountain West',
    'UT': 'Mountain West',
    'NV': 'Mountain West',
    'ID': 'Mountain West',
    'MT': 'Mountain West',
    'WY': 'Mountain West',
    
    # Pacific
    'HI': 'Pacific',
    'AK': 'Pacific',
}

# ============================================================================
# DATA PROCESSING PARAMETERS
# ============================================================================

# Deal size categories for bucketing
DEAL_SIZE_BUCKETS = [
    ('Micro (<$1M)', 0, 1_000_000),
    ('Seed ($1-5M)', 1_000_000, 5_000_000),
    ('Series A ($5-10M)', 5_000_000, 10_000_000),
    ('Series B ($10-25M)', 10_000_000, 25_000_000),
    ('Series C ($25-50M)', 25_000_000, 50_000_000),
    ('Growth ($50-100M)', 50_000_000, 100_000_000),
    ('Large ($100M+)', 100_000_000, float('inf'))
]

# Fields that indicate "Indefinite" or unlimited amounts
INDEFINITE_VALUES = ['Indefinite', 'INDEFINITE', 'Unlimited', 'UNLIMITED', '']

# Date format used in Form D filings
FILING_DATE_FORMAT = '%d-%b-%Y'  # e.g., '31-DEC-2025'

# Minimum data quality thresholds
MIN_REQUIRED_FIELDS = [
    'ACCESSIONNUMBER',
    'FILING_DATE',
    'ENTITYNAME',
    'STATEORCOUNTRY',
    'TOTALOFFERINGAMOUNT'
]

# ============================================================================
# VISUALIZATION SETTINGS
# ============================================================================

# Color palette (professional VC theme)
COLOR_PALETTE = {
    'primary': '#1f77b4',      # Blue
    'secondary': '#ff7f0e',    # Orange
    'success': '#2ca02c',      # Green
    'warning': '#d62728',      # Red
    'info': '#9467bd',         # Purple
    'neutral': '#7f7f7f'       # Gray
}

# Chart settings
CHART_STYLE = 'seaborn-v0_8-darkgrid'
FIGURE_DPI = 300
FIGURE_SIZE = (12, 6)

# ============================================================================
# OUTPUT SETTINGS
# ============================================================================

# Number of top targets to generate
TOP_TARGETS_COUNT = 50

# Minimum score for target list inclusion
MIN_TARGET_SCORE = 60  # out of 100

# Analysis time window (months back from most recent data)
ANALYSIS_WINDOW_MONTHS = 18

# Export formats
EXPORT_FORMATS = ['csv', 'excel', 'json']
