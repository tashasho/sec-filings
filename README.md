# SEC Form D Analysis - VC Market Intelligence Platform

A comprehensive analytical pipeline to analyze SEC Form D filings, providing actionable investment intelligence for venture capital decision-making.

## Overview

This project analyzes **111,259 Form D filings** from 2024-2025 to surface:
- Market trends in private capital markets
- Sector dynamics and growth patterns
- Geographic investment patterns
- Scored target company list for deal sourcing

## Key Findings

- **Total Capital Raised**: $24.2T across all offerings (including funds)
- **Operating Company Deals**: 43,335 offerings
- **Investment Funds**: 67,924 fund formations
- **Top Sectors**: Biotech (1,556), Energy (1,064), Insurtech (782)
- **Deal Size Sweet Spot**: $10-25M (Series B range)

## Project Structure

```
├── analysis/                      # Analysis code
│   ├── config.py                  # Configuration & sector mappings
│   ├── data_loader.py             # Data loading pipeline
│   ├── data_cleaning.py           # Cleaning & transformation
│   ├── temporal_analysis.py       # Time series analysis
│   ├── sector_analysis.py         # Sector intelligence
│   ├── target_generator.py        # Opportunity scoring
│   └── run_pipeline.py            # Master pipeline script
├── reports/
│   ├── executive_summary.md       # Executive summary
│   ├── data_quality_report.txt    # Data quality documentation
│   └── target_companies.csv       # Scored target list
├── visualizations/
│   ├── temporal/                  # 4 time series charts
│   └── sector/                    # 5 sector analysis charts
├── tests/                         # Test suite
└── README.md
```

## Quick Start

### Prerequisites
- Python 3.10+
- pandas, numpy, matplotlib, seaborn

### Run the Pipeline

```bash
# 1. Download Form D data from SEC
# Place quarterly data in directories: 2024Q1_d/, 2024Q2_d/, etc.

# 2. Run the full pipeline
python3 analysis/run_pipeline.py

# 3. Run temporal analysis
python3 analysis/temporal_analysis.py

# 4. Run sector analysis
python3 analysis/sector_analysis.py

# 5. Generate target company list
python3 analysis/target_generator.py
```

## Data Source

[SEC Form D Data Sets](https://www.sec.gov/data-research/sec-markets-data/form-d-data-sets)

## Deliverables

| Deliverable | Location |
|-------------|----------|
| Executive Summary | `reports/executive_summary.md` |
| Target Companies | `reports/target_companies.csv` |
| Data Quality Report | `reports/data_quality_report.txt` |
| Temporal Charts (4) | `visualizations/temporal/` |
| Sector Charts (5) | `visualizations/sector/` |

## Strategic Recommendations

1. **Sector Focus**: Biotech (MA, CA), Energy Transition (TX, CA, CO), Enterprise AI
2. **Geography**: 50% tier-1 hubs + 30% secondary markets (Austin, Denver, Miami)
3. **Deal Size**: Target $5-25M range (Series A/B)
4. **Quality Filters**: Multiple investors, placement agents, follow-on rounds

## License

MIT
