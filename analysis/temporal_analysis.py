"""
Temporal Trends Analysis for SEC Form D Filings
Analyzes deal volume and capital raised over time
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Dict
import logging

# Set visualization style
sns.set_style("darkgrid")
plt.rcParams['figure.figsize'] = (14, 6)
plt.rcParams['figure.dpi'] = 100

logger = logging.getLogger(__name__)


class TemporalAnalyzer:
    """
    Analyzes temporal trends in Form D filings
    """
    
    def __init__(self, analytical_df: pd.DataFrame):
        """
        Initialize analyzer with analytical dataset
        
        Args:
            analytical_df: Cleaned analytical dataframe
        """
        self.df = analytical_df.copy()
        self.figures = []
        
        # Filter out funds for operating company analysis
        self.operating_df = self.df[~self.df['is_fund']].copy()
        
    def analyze_all(self, output_dir: str):
        """
        Run all temporal analyses and save visualizations
        
        Args:
            output_dir: Directory to save charts
        """
        logger.info("=" * 70)
        logger.info("TEMPORAL TRENDS ANALYSIS")
        logger.info("=" * 70)
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Quarterly volume and capital
        self.quarterly_volume_capital(output_path)
        
        # Monthly trends
        self.monthly_trends(output_path)
        
        # YoY and QoQ growth
        self.growth_rates(output_path)
        
        # Deal volume vs median size over time
        self.volume_size_dual_axis(output_path)
        
        logger.info(f"\n✓ Saved {len(self.figures)} visualizations to {output_path}")
        
    def quarterly_volume_capital(self, output_path: Path):
        """
        Quarterly deal volume and capital raised
        """
        logger.info("\nAnalyzing quarterly trends...")
        
        # Aggregate by quarter - exclude funds for clearer operating company trends
        quarterly = self.operating_df.groupby(['filing_year', 'filing_quarter']).agg({
            'ACCESSIONNUMBER': 'count',
            'total_amount_sold': 'sum',
            'total_offering_amount': ['median', 'mean']
        }).reset_index()
        
        quarterly.columns = ['year', 'quarter', 'deal_count', 'capital_raised', 'median_size', 'mean_size']
        quarterly['period'] = quarterly['year'].astype(str) + '-Q' + quarterly['quarter'].astype(str)
        quarterly['capital_raised_b'] = quarterly['capital_raised'] / 1e9
        
        # Create subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Deal count
        ax1.bar(range(len(quarterly)), quarterly['deal_count'], color='#2E86AB', alpha=0.8)
        ax1.set_xticks(range(len(quarterly)))
        ax1.set_xticklabels(quarterly['period'], rotation=45)
        ax1.set_ylabel('Number of Deals', fontsize=12, fontweight='bold')
        ax1.set_title('Quarterly Deal Volume\n(Operating Companies Only)', fontsize=14, fontweight='bold')
        ax1.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for i, v in enumerate(quarterly['deal_count']):
            ax1.text(i, v, f'{v:,}', ha='center', va='bottom', fontsize=9)
        
        # Capital raised
        ax2.bar(range(len(quarterly)), quarterly['capital_raised_b'], color='#A23B72', alpha=0.8)
        ax2.set_xticks(range(len(quarterly)))
        ax2.set_xticklabels(quarterly['period'], rotation=45)
        ax2.set_ylabel('Capital Raised ($B)', fontsize=12, fontweight='bold')
        ax2.set_title('Quarterly Capital Raised\n(Operating Companies Only)', fontsize=14, fontweight='bold')
        ax2.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for i, v in enumerate(quarterly['capital_raised_b']):
            ax2.text(i, v, f'${v:.1f}B', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        fig_path = output_path / 'temporal_quarterly_volume_capital.png'
        plt.savefig(fig_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"  ✓ Saved: {fig_path.name}")
        self.figures.append(fig_path)
        
        # Print summary stats
        logger.info(f"  Average quarterly deals: {quarterly['deal_count'].mean():.0f}")
        logger.info(f"  Average quarterly capital: ${quarterly['capital_raised_b'].mean():.1f}B")
        
    def monthly_trends(self, output_path: Path):
        """
        Monthly deal activity and seasonality
        """
        logger.info("\nAnalyzing monthly trends...")
        
        # Aggregate by year-month
        self.operating_df['year_month'] = self.operating_df['filing_date'].dt.to_period('M')
        monthly = self.operating_df.groupby('year_month').agg({
            'ACCESSIONNUMBER': 'count',
            'total_amount_sold': 'sum'
        }).reset_index()
        
        monthly.columns = ['year_month', 'deal_count', 'capital_raised']
        monthly['year_month_str'] = monthly['year_month'].astype(str)
        monthly['capital_raised_b'] = monthly['capital_raised'] / 1e9
        
        # Plot
        fig, ax = plt.subplots(figsize=(16, 6))
        
        ax.plot(range(len(monthly)), monthly['deal_count'], marker='o', linewidth=2, 
                color='#2E86AB', label='Deal Count')
        ax.set_xticks(range(0, len(monthly), 3))  # Show every 3 months
        ax.set_xticklabels(monthly['year_month_str'].iloc[::3], rotation=45)
        ax.set_ylabel('Number of Deals', fontsize=12, fontweight='bold')
        ax.set_title('Monthly Deal Volume Trend (Operating Companies)', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=10)
        
        plt.tight_layout()
        fig_path = output_path / 'temporal_monthly_trends.png'
        plt.savefig(fig_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"  ✓ Saved: {fig_path.name}")
        self.figures.append(fig_path)
        
    def growth_rates(self, output_path: Path):
        """
        Calculate and visualize QoQ and YoY growth rates
        """
        logger.info("\nCalculating growth rates...")
        
        # Quarterly data
        quarterly = self.operating_df.groupby(['filing_year', 'filing_quarter']).agg({
            'ACCESSIONNUMBER': 'count',
            'total_amount_sold': 'sum'
        }).reset_index()
        
        quarterly.columns = ['year', 'quarter', 'deal_count', 'capital_raised']
        quarterly = quarterly.sort_values(['year', 'quarter'])
        quarterly['period'] = quarterly['year'].astype(str) + '-Q' + quarterly['quarter'].astype(str)
        
        # Calculate QoQ growth
        quarterly['deal_count_qoq'] = quarterly['deal_count'].pct_change() * 100
        quarterly['capital_qoq'] = quarterly['capital_raised'].pct_change() * 100
        
        # Plot growth rates
        fig, ax = plt.subplots(figsize=(14, 6))
        
        x = range(1, len(quarterly))  # Skip first quarter (no previous data)
        width = 0.35
        
        ax.bar([i - width/2 for i in x], quarterly['deal_count_qoq'].iloc[1:], 
               width, label='Deal Volume Growth', color='#2E86AB', alpha=0.8)
        ax.bar([i + width/2 for i in x], quarterly['capital_qoq'].iloc[1:], 
               width, label='Capital Raised Growth', color='#A23B72', alpha=0.8)
        
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
        ax.set_xticks(x)
        ax.set_xticklabels(quarterly['period'].iloc[1:], rotation=45)
        ax.set_ylabel('Growth Rate (%)', fontsize=12, fontweight='bold')
        ax.set_title('Quarter-over-Quarter Growth Rates (Operating Companies)', fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        fig_path = output_path / 'temporal_growth_rates.png'
        plt.savefig(fig_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"  ✓ Saved: {fig_path.name}")
        self.figures.append(fig_path)
        
        # Print growth summary
        avg_qoq_deals = quarterly['deal_count_qoq'].iloc[1:].mean()
        avg_qoq_capital = quarterly['capital_qoq'].iloc[1:].mean()
        logger.info(f"  Avg QoQ deal volume growth: {avg_qoq_deals:.1f}%")
        logger.info(f"  Avg QoQ capital growth: {avg_qoq_capital:.1f}%")
        
    def volume_size_dual_axis(self, output_path: Path):
        """
        Dual-axis chart: Deal volume vs median deal size
        """
        logger.info("\nCreating volume vs size chart...")
        
        # Quarterly aggregation
        quarterly = self.operating_df.groupby(['filing_year', 'filing_quarter']).agg({
            'ACCESSIONNUMBER': 'count',
            'total_offering_amount': 'median'
        }).reset_index()
        
        quarterly.columns = ['year', 'quarter', 'deal_count', 'median_size']
        quarterly['period'] = quarterly['year'].astype(str) + '-Q' + quarterly['quarter'].astype(str)
        quarterly['median_size_m'] = quarterly['median_size'] / 1e6
        
        # Create dual-axis plot
        fig, ax1 = plt.subplots(figsize=(14, 6))
        
        color1 = '#2E86AB'
        ax1.set_xlabel('Quarter', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Number of Deals', fontsize=12, fontweight='bold', color=color1)
        ax1.bar(range(len(quarterly)), quarterly['deal_count'], color=color1, alpha=0.6, label='Deal Volume')
        ax1.tick_params(axis='y', labelcolor=color1)
        ax1.set_xticks(range(len(quarterly)))
        ax1.set_xticklabels(quarterly['period'], rotation=45)
        
        # Second y-axis
        ax2 = ax1.twinx()
        color2 = '#F18F01'
        ax2.set_ylabel('Median Deal Size ($M)', fontsize=12, fontweight='bold', color=color2)
        ax2.plot(range(len(quarterly)), quarterly['median_size_m'], color=color2, 
                marker='o', linewidth=2.5, markersize=8, label='Median Size')
        ax2.tick_params(axis='y', labelcolor=color2)
        
        fig.legend(loc='upper left', bbox_to_anchor=(0.12, 0.9), fontsize=10)
        plt.title('Deal Volume vs Median Deal Size Over Time\n(Operating Companies)', 
                 fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        fig_path = output_path / 'temporal_volume_vs_size.png'
        plt.savefig(fig_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"  ✓ Saved: {fig_path.name}")
        self.figures.append(fig_path)


def main():
    """
    Run temporal analysis on cleaned data
    """
    base_path = Path("/Users/bhumikamarmat/sec filings")
    data_path = base_path / "data" / "cleaned_analytical.csv"
    
    print("Loading analytical dataset...")
    df = pd.read_csv(data_path, parse_dates=['filing_date', 'sale_date'])
    
    print(f"Loaded {len(df):,} offerings")
    
    # Run analysis
    analyzer = TemporalAnalyzer(df)
    viz_path = base_path / "visualizations" / "temporal"
    analyzer.analyze_all(str(viz_path))
    
    print("\n✓ Temporal analysis complete!")


if __name__ == "__main__":
    main()
