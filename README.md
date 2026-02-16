# SEC Form D Private Markets Analysis

> **18-Year Longitudinal Study of U.S. Exempt Offerings (2008–2025)**  
> An analytical toolkit for investment professionals studying private capital formation trends.

## Overview

This repository contains a comprehensive analysis pipeline for SEC Form D filings — the regulatory disclosures required for private securities offerings in the United States. The analysis covers **730,640 filings** across **72 quarters** (2008Q1–2025Q4), representing the most complete publicly available dataset on U.S. private capital markets.

### Key Metrics

| Metric | Value |
|---|---|
| Total Filings Analyzed | 730,640 |
| Unique Issuers | 354,645 |
| Date Range | Jan 2008 – Dec 2025 |
| Investment Funds | 387,257 (53%) |
| Operating Companies | 343,383 (47%) |
| Target Companies Identified | 43 |

## Repository Structure

```
sec-filings/
├── analysis/                    # Python analysis modules
│   ├── config.py               # Configuration & sector mappings
│   ├── data_loader.py          # Multi-format quarterly data loader
│   ├── data_cleaning.py        # Cleaning, feature engineering
│   ├── run_pipeline.py         # Pipeline orchestrator
│   ├── temporal_analysis.py    # Time-series analysis & visualizations
│   ├── sector_analysis.py      # Sector analysis & visualizations
│   ├── target_generator.py     # Scoring model for investment targets
│   └── download_sec_data.py    # SEC EDGAR data downloader
├── reports/                     # Generated reports
│   ├── executive_summary.md    # Executive summary (2008-2025)
│   ├── market_analysis_report.md # Detailed market analysis
│   ├── target_companies.csv    # Scored target company list
│   └── data_quality_report.txt # Data validation results
├── visualizations/              # Generated charts
│   ├── temporal/               # 4 time-series visualizations
│   └── sector/                 # 5 sector analysis charts
├── 2008/ - 2025/               # Raw SEC data (not in repo)
└── data/                       # Processed datasets (not in repo)
```

## Quick Start

### Prerequisites
```bash
pip install pandas numpy matplotlib seaborn
```

### 1. Download Data
```bash
python analysis/download_sec_data.py    # Downloads 2008-2021 from SEC
```

### 2. Run Pipeline
```bash
python analysis/run_pipeline.py         # Load + clean all quarters
```

### 3. Run Analysis
```bash
python analysis/temporal_analysis.py    # Temporal trends & growth
python analysis/sector_analysis.py      # Sector distribution & capital
python analysis/target_generator.py     # Score and rank targets
```

## Data Sources

All data is sourced directly from [SEC EDGAR Form D Data Sets](https://www.sec.gov/data-research/sec-markets-data/form-d-data-sets), which are released quarterly. Each quarter contains:

- **FORMDSUBMISSION.tsv** — Filing metadata, dates, SIC codes
- **ISSUERS.tsv** — Company information, state, entity type
- **OFFERING.tsv** — Offering details, amounts, exemptions, investors
- **RELATEDPERSONS.tsv** — Directors, officers, promoters
- **RECIPIENTS.tsv** — Sales compensation recipients
- **SIGNATURES.tsv** — Authorized signers

## Key Findings

1. **Market Growth**: Filing volumes grew from ~21K (2009) to ~56K (2025), a 2.7x increase
2. **COVID Resilience**: Only a 12.6% Q2 2020 dip, with V-shaped recovery
3. **Post-COVID Boom**: 2021-2022 saw record volumes (62K+), driven by SPAC/VC activity
4. **506(b) Dominance**: 91% of filings use Rule 506(b) vs only 7% for 506(c)
5. **Geographic Shift**: NY+CA share declined from 42% to 36% as FL, CO, WA grow
6. **Biotech Pipeline**: Most target-rich sector for operating company investments

## Analysis Modules

### Data Loader (`data_loader.py`)
Handles three directory structures across the 18-year dataset:
- **2008-2021**: Double-nested from zip extraction
- **2022-2023**: Year-nested quarterly directories
- **2024-2025**: Top-level quarterly directories

### Data Cleaning (`data_cleaning.py`)
- Flexible date parsing (mixed formats with quarter-metadata fallback)
- Sector mapping (SEC Industry Group → 12-sector taxonomy)
- Deal size categorization (Micro through Large)
- Fund classification (Hedge, PE, VC, Other)

### Target Generator (`target_generator.py`)
Multi-factor scoring model:
- **Sector Fit** (25%) — Alignment with thesis sectors
- **Momentum** (25%) — Follow-on filings, investor growth
- **Deal Size** (20%) — $5-25M sweet spot
- **Geography** (15%) — Innovation hub proximity
- **Quality** (15%) — Placement agents, team size

## Visualizations

| Chart | Description |
|---|---|
| `temporal_quarterly_volume_capital.png` | 72-quarter filing volume and capital trends |
| `temporal_monthly_trends.png` | Monthly seasonality patterns |
| `temporal_growth_rates.png` | Year-over-year and quarter-over-quarter growth |
| `temporal_volume_vs_size.png` | Deal volume vs median offering size |
| `sector_distribution.png` | Sector filing distribution |
| `sector_capital.png` | Capital raised by sector |
| `sector_growth.png` | Sector growth rates over time |
| `sector_concentration.png` | Market concentration metrics |
| `sector_deal_sizes.png` | Deal size distributions by sector |

## License

This analysis uses publicly available SEC data. The code in this repository is provided for educational and analytical purposes.

---

*Built by Z5 Capital | Data: SEC EDGAR | Analysis: Python (pandas, matplotlib, seaborn)*
