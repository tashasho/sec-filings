"""
Sector Analysis for SEC Form D Filings
Analyzes industry distribution, growth, and concentration
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Dict, List
import logging

sns.set_style("darkgrid")
plt.rcParams['figure.figsize'] = (14, 8)

logger = logging.getLogger(__name__)


class SectorAnalyzer:
    """
    Analyzes sector distribution and dynamics
    """
    
    def __init__(self, analytical_df: pd.DataFrame):
        """
        Initialize with analytical dataset
        """
        self.df = analytical_df.copy()
        self.operating_df = self.df[~self.df['is_fund']].copy()
        self.figures = []
        
    def analyze_all(self, output_dir: str):
        """
        Run all sector analyses
        """
        logger.info("=" * 70)
        logger.info("SECTOR ANALYSIS")
        logger.info("=" * 70)
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Sector distribution
        self.sector_distribution(output_path)
        
        # Capital by sector
        self.capital_by_sector(output_path)
        
        # Sector growth rates
        self.sector_growth(output_path)
        
        # Sector concentration
        self.sector_concentration(output_path)
        
        # Sector size comparison
        self.sector_deal_sizes(output_path)
        
        logger.info(f"\n✓ Saved {len(self.figures)} visualizations to {output_path}")
        
    def sector_distribution(self, output_path: Path):
        """
        Distribution of deals by sector
        """
        logger.info("\nAnalyzing sector distribution...")
        
        # Count by sector
        sector_counts = self.operating_df['sector'].value_counts().head(15)
        
        # Create bar chart
        fig, ax = plt.subplots(figsize=(12, 8))
        
        colors = plt.cm.tab20(np.linspace(0, 1, len(sector_counts)))
        bars = ax.barh(range(len(sector_counts)), sector_counts.values, color=colors, alpha=0.8)
        
        ax.set_yticks(range(len(sector_counts)))
        ax.set_yticklabels(sector_counts.index, fontsize=11)
        ax.set_xlabel('Number of Deals', fontsize=12, fontweight='bold')
        ax.set_title('Deal Distribution by Sector (Top 15)\nOperating Companies Only', 
                     fontsize=14, fontweight='bold', pad=15)
        ax.grid(axis='x', alpha=0.3)
        
        # Add value labels
        for i, (bar, value) in enumerate(zip(bars, sector_counts.values)):
            ax.text(value, bar.get_y() + bar.get_height()/2, 
                   f'  {value:,}', va='center', fontsize=9)
        
        plt.tight_layout()
        fig_path = output_path / 'sector_distribution.png'
        plt.savefig(fig_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"  ✓ Saved: {fig_path.name}")
        self.figures.append(fig_path)
        
        # Print top sectors
        logger.info(f"  Top 5 sectors:")
        for sector, count in sector_counts.head(5).items():
            pct = (count / len(self.operating_df)) * 100
            logger.info(f"    {sector}: {count:,} ({pct:.1f}%)")
            
    def capital_by_sector(self, output_path: Path):
        """
        Capital raised by sector
        """
        logger.info("\nAnalyzing capital by sector...")
        
        # Aggregate capital and median size by sector
        sector_stats = self.operating_df.groupby('sector').agg({
            'total_amount_sold': ['sum', 'median', 'count']
        }).reset_index()
        
        sector_stats.columns = ['sector', 'total_capital', 'median_size', 'deal_count']
        sector_stats['total_capital_b'] = sector_stats['total_capital'] / 1e9
        sector_stats['median_size_m'] = sector_stats['median_size'] / 1e6
        sector_stats = sector_stats.sort_values('total_capital', ascending=False).head(15)
        
        # Create figure with two subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # Total capital
        colors1 = plt.cm.Purples(np.linspace(0.4, 0.9, len(sector_stats)))
        bars1 = ax1.barh(range(len(sector_stats)), sector_stats['total_capital_b'], 
                         color=colors1, alpha=0.8)
        ax1.set_yticks(range(len(sector_stats)))
        ax1.set_yticklabels(sector_stats['sector'], fontsize=10)
        ax1.set_xlabel('Total Capital Raised ($B)', fontsize=12, fontweight='bold')
        ax1.set_title('Total Capital Raised by Sector\n(Top 15)', fontsize=13, fontweight='bold')
        ax1.grid(axis='x', alpha=0.3)
        
        for i, (bar, value) in enumerate(zip(bars1, sector_stats['total_capital_b'])):
            ax1.text(value, bar.get_y() + bar.get_height()/2, 
                    f'  ${value:.1f}B', va='center', fontsize=9)
        
        # Median deal size
        colors2 = plt.cm.Blues(np.linspace(0.4, 0.9, len(sector_stats)))
        bars2 = ax2.barh(range(len(sector_stats)), sector_stats['median_size_m'], 
                         color=colors2, alpha=0.8)
        ax2.set_yticks(range(len(sector_stats)))
        ax2.set_yticklabels(sector_stats['sector'], fontsize=10)
        ax2.set_xlabel('Median Deal Size ($M)', fontsize=12, fontweight='bold')
        ax2.set_title('Median Deal Size by Sector\n(Top 15)', fontsize=13, fontweight='bold')
        ax2.grid(axis='x', alpha=0.3)
        
        for i, (bar, value) in enumerate(zip(bars2, sector_stats['median_size_m'])):
            ax2.text(value, bar.get_y() + bar.get_height()/2, 
                    f'  ${value:.1f}M', va='center', fontsize=9)
        
        plt.tight_layout()
        fig_path = output_path / 'sector_capital.png'
        plt.savefig(fig_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"  ✓ Saved: {fig_path.name}")
        self.figures.append(fig_path)
        
    def sector_growth(self, output_path: Path):
        """
        Sector growth rates YoY
        """
        logger.info("\nAnalyzing sector growth...")
        
        # Count by sector and year
        sector_year = self.operating_df.groupby(['sector', 'filing_year']).size().reset_index(name='count')
        
        # Pivot to calculate YoY growth
        pivot = sector_year.pivot(index='sector', columns='filing_year', values='count').fillna(0)
        
        if len(pivot.columns) >= 2:
            # Calculate growth from first to last year
            first_year = pivot.columns[0]
            last_year = pivot.columns[-1]
            
            pivot['growth_pct'] = ((pivot[last_year] - pivot[first_year]) / 
                                  (pivot[first_year] + 1)) * 100  # +1 to avoid div by zero
            
            # Filter sectors with meaningful activity
            pivot_filtered = pivot[pivot[last_year] >= 10].sort_values('growth_pct', ascending=False).head(15)
            
            # Plot
            fig, ax = plt.subplots(figsize=(12, 8))
            
            colors = ['#2E86AB' if x >= 0 else '#D62828' for x in pivot_filtered['growth_pct']]
            bars = ax.barh(range(len(pivot_filtered)), pivot_filtered['growth_pct'], 
                          color=colors, alpha=0.8)
            
            ax.set_yticks(range(len(pivot_filtered)))
            ax.set_yticklabels(pivot_filtered.index, fontsize=10)
            ax.set_xlabel(f'Growth Rate (%) from {first_year} to {last_year}', fontsize=12, fontweight='bold')
            ax.set_title(f'Sector Growth Rates: {first_year} to {last_year}\n(Operating Companies)', 
                        fontsize=14, fontweight='bold', pad=15)
            ax.axvline(x=0, color='black', linestyle='-', linewidth=1)
            ax.grid(axis='x', alpha=0.3)
            
            # Add value labels
            for i, (bar, value) in enumerate(zip(bars, pivot_filtered['growth_pct'])):
                ax.text(value, bar.get_y() + bar.get_height()/2, 
                       f'  {value:.1f}%', va='center', fontsize=9)
            
            plt.tight_layout()
            fig_path = output_path / 'sector_growth.png'
            plt.savefig(fig_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"  ✓ Saved: {fig_path.name}")
            self.figures.append(fig_path)
        else:
            logger.warning("  Insufficient years for growth analysis")
            
    def sector_concentration(self, output_path: Path):
        """
        Sector concentration metrics (HHI and top-N)
        """
        logger.info("\nCalculating sector concentration...")
        
        sector_counts = self.operating_df['sector'].value_counts()
        total_deals = len(self.operating_df)
        
        # Market shares
        market_shares = (sector_counts / total_deals) * 100
        
        # Herfindahl-Hirschman Index (HHI)
        hhi = (market_shares ** 2).sum()
        
        # Top-5 concentration
        top5_concentration = market_shares.head(5).sum()
        
        logger.info(f"  HHI Index: {hhi:.1f}")
        logger.info(f"  Top-5 Concentration: {top5_concentration:.1f}%")
        
        # Pie chart for top sectors
        top_sectors = sector_counts.head(10)
        other_count = sector_counts.iloc[10:].sum() if len(sector_counts) > 10 else 0
        
        if other_count > 0:
            top_sectors['Other'] = other_count
        
        fig, ax = plt.subplots(figsize=(12, 10))
        
        colors = plt.cm.tab20(np.linspace(0, 1, len(top_sectors)))
        wedges, texts, autotexts = ax.pie(top_sectors.values, labels=top_sectors.index, 
                                          autopct='%1.1f%%', colors=colors, startangle=90,
                                          textprops={'fontsize': 10})
        
        # Make percentage text bold
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(9)
        
        ax.set_title(f'Sector Concentration (Top 10 + Other)\nHHI: {hhi:.1f} | Top-5: {top5_concentration:.1f}%', 
                     fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        fig_path = output_path / 'sector_concentration.png'
        plt.savefig(fig_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"  ✓ Saved: {fig_path.name}")
        self.figures.append(fig_path)
        
    def sector_deal_sizes(self, output_path: Path):
        """
        Compare deal sizes across sectors
        """
        logger.info("\nAnalyzing deal sizes by sector...")
        
        # Filter top sectors for cleaner visualization
        top_sectors = self.operating_df['sector'].value_counts().head(10).index
        df_filtered = self.operating_df[self.operating_df['sector'].isin(top_sectors)].copy()
        
        # Remove outliers for better visualization (keep reasonable offering amounts)
        df_filtered = df_filtered[
            (df_filtered['total_offering_amount'] > 0) & 
            (df_filtered['total_offering_amount'] < 1e9)  # < $1B
        ]
        
        # Box plot
        fig, ax = plt.subplots(figsize=(14, 8))
        
        df_filtered['offering_amount_m'] = df_filtered['total_offering_amount'] / 1e6
        
        sector_order = df_filtered.groupby('sector')['offering_amount_m'].median().sort_values(ascending=False).index
        
        box_plot = sns.boxplot(data=df_filtered, y='sector', x='offering_amount_m', 
                               order=sector_order, palette='Set2', ax=ax)
        
        ax.set_xlabel('Offering Amount ($M)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Sector', fontsize=12, fontweight='bold')
        ax.set_title('Deal Size Distribution by Sector (Top 10)\nOperating Companies', 
                     fontsize=14, fontweight='bold', pad=15)
        ax.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        fig_path = output_path / 'sector_deal_sizes.png'
        plt.savefig(fig_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"  ✓ Saved: {fig_path.name}")
        self.figures.append(fig_path)


def main():
    """
    Run sector analysis
    """
    base_path = Path("/Users/bhumikamarmat/sec filings")
    data_path = base_path / "data" / "cleaned_analytical.csv"
    
    print("Loading analytical dataset...")
    df = pd.read_csv(data_path, parse_dates=['filing_date', 'sale_date'])
    
    print(f"Loaded {len(df):,} offerings")
    
    # Run analysis
    analyzer = SectorAnalyzer(df)
    viz_path = base_path / "visualizations" / "sector"
    analyzer.analyze_all(str(viz_path))
    
    print("\n✓ Sector analysis complete!")


if __name__ == "__main__":
    main()
