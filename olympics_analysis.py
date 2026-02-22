"""
============================================================
 OLYMPIC GAMES DATA ANALYSIS PROJECT
 A Beginner-to-Advanced Python Project for Data Engineers
============================================================

SKILLS COVERED:
- Python OOP (Classes, Inheritance, Methods, Properties)
- Pandas (Loading, Cleaning, Grouping, Merging, Aggregating)
- NumPy (Array operations, Statistical computations)
- Matplotlib & Seaborn (Charts, Subplots, Customization)
- Data Engineering Concepts (ETL, Pipelines, Reusability)

PROJECT STRUCTURE:
  Module 1 (Beginner)   → Data Loading & Basic Exploration
  Module 2 (Beginner+)  → Data Cleaning & Preprocessing (OOP)
  Module 3 (Intermediate) → Medal Tally & Country Analysis
  Module 4 (Intermediate+) → Athlete & Sport Analytics
  Module 5 (Advanced)   → Advanced Analytics, Trends & Reporting Pipeline

RUN THIS FILE:  python olympics_analysis.py
"""

# ─────────────────────────────────────────
# IMPORTS
# ─────────────────────────────────────────
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import warnings
import os
import openpyxl

warnings.filterwarnings('ignore')

# ── Path Setup ──────────────────────────────────────────────
# __file__ is the full path of THIS script, e.g.:
#   /Users/harika/Documents/Python Practice/Olympics Project/olympics_analysis.py
#
# os.path.dirname(__file__) gets the FOLDER the script lives in.
# os.path.join() then builds paths RELATIVE to that folder.
# This means it always works no matter which directory your terminal is in.

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def path(filename):
    """Helper: build a full path relative to this script s folder."""
    return os.path.join(BASE_DIR, filename)

# Create output folders next to the script
os.makedirs(path("output_charts"), exist_ok=True)
os.makedirs(path("output_reports"), exist_ok=True)

print("=" * 60)
print("  OLYMPIC GAMES ANALYSIS PROJECT")
print("  From Beginner to Advanced with Python")
print("=" * 60)


# ╔══════════════════════════════════════════════════════════╗
# ║  MODULE 1 — DATA LOADING & BASIC EXPLORATION (Beginner) ║
# ╚══════════════════════════════════════════════════════════╝
"""
LEARNING GOALS:
- How to load CSV/Excel files using pandas
- Basic DataFrame inspection methods
- Understanding data types and structure
- Using numpy for quick stats
"""

print("\n" + "─" * 60)
print("  MODULE 1: DATA LOADING & BASIC EXPLORATION")
print("─" * 60)


# ── Step 1: Load the dataset ────────────────────────────────
# pd.read_csv() reads a CSV file into a pandas DataFrame
# A DataFrame is like an Excel table — rows and columns
df = pd.read_csv(path("olympics_data.csv"))
country_df = pd.read_csv(path("country_info.csv"))

print("\n✅ Data loaded successfully!")

# ── Step 2: Basic inspection ────────────────────────────────
print("\n📌 First 5 rows of the dataset:")
print(df.head())  # Shows first 5 rows

print("\n📌 Shape (rows, columns):", df.shape)

print("\n📌 Column names:")
print(df.columns.tolist())

print("\n📌 Data types of each column:")
print(df.dtypes)

print("\n📌 Basic statistics using describe():")
print(df.describe())  # gives count, mean, std, min, max for numeric cols

print("\n📌 Missing values per column:")
print(df.isnull().sum())  # Count of NaN values per column

# ── Step 3: NumPy quick stats ────────────────────────────────
"""
NumPy works on arrays. pandas Series can be converted to numpy arrays.
"""
ages = df['age'].dropna().values  # .values converts to numpy array

print("\n📌 NumPy Statistics on Athlete Ages:")
print(f"  Mean age     : {np.mean(ages):.2f}")
print(f"  Median age   : {np.median(ages):.2f}")
print(f"  Std deviation: {np.std(ages):.2f}")
print(f"  Min / Max    : {np.min(ages)} / {np.max(ages)}")
print(f"  25th percentile: {np.percentile(ages, 25):.2f}")
print(f"  75th percentile: {np.percentile(ages, 75):.2f}")

# ── Step 4: Unique value counts ─────────────────────────────
print("\n📌 Number of unique values:")
for col in ['sport', 'team', 'year', 'medal', 'city']:
    print(f"  {col:<12}: {df[col].nunique()} unique values")


# ╔══════════════════════════════════════════════════════════╗
# ║  MODULE 2 — DATA CLEANING & OOP INTRO (Beginner+)       ║
# ╚══════════════════════════════════════════════════════════╝
"""
LEARNING GOALS:
- What is a Class? Why use OOP?
- Creating a DataLoader class (Encapsulation)
- Cleaning data: handling missing values, duplicates, types
- Building reusable utility functions as methods
"""

print("\n" + "─" * 60)
print("  MODULE 2: DATA CLEANING WITH OOP")
print("─" * 60)


class OlympicsDataLoader:
    """
    A class to load and clean Olympics data.
    
    OOP CONCEPT: Encapsulation
    - All data-related logic is inside this class
    - You call methods on the object instead of scattered functions
    - Makes code reusable and organized
    """

    def __init__(self, filepath: str, country_filepath: str):
        """
        __init__ is the constructor — called when you create an object.
        'self' refers to the object itself.
        """
        self.filepath = filepath
        self.country_filepath = country_filepath
        self.df = None          # Will hold our main dataset
        self.country_df = None  # Will hold country info
        self._is_loaded = False  # Private attribute (convention: _ prefix)

    def load(self):
        """Load raw data from CSV files."""
        print("\n[DataLoader] Loading data...")
        self.df = pd.read_csv(self.filepath)
        self.country_df = pd.read_csv(self.country_filepath)
        self._is_loaded = True
        print(f"[DataLoader] ✅ Loaded {len(self.df):,} records")
        return self  # Return self so we can chain methods

    def clean(self):
        """
        Clean the data:
        - Remove duplicates
        - Handle missing values
        - Fix data types
        - Add derived columns
        """
        if not self._is_loaded:
            raise RuntimeError("Call load() first before clean()!")

        print("\n[DataLoader] Cleaning data...")
        before = len(self.df)

        # 1. Remove duplicate rows
        self.df = self.df.drop_duplicates()

        # 2. Fill missing numeric values with median
        for col in ['age', 'height_cm', 'weight_kg']:
            median_val = self.df[col].median()
            self.df[col] = self.df[col].fillna(median_val)

        # 3. Ensure proper types
        self.df['year'] = self.df['year'].astype(int)
        self.df['age'] = self.df['age'].astype(int)

        # 4. Add a BMI column (derived feature — common in data engineering)
        # BMI = weight(kg) / height(m)^2
        self.df['bmi'] = (
            self.df['weight_kg'] / ((self.df['height_cm'] / 100) ** 2)
        ).round(2)

        # 5. Add era column (useful for grouping historical analysis)
        bins = [1895, 1920, 1950, 1980, 2000, 2025]
        labels = ['Early Era\n(1896-1920)', 'Pre-War Era\n(1924-1950)',
                  'Cold War Era\n(1952-1980)', 'Modern Era\n(1984-2000)',
                  'Contemporary\n(2004-2024)']
        self.df['era'] = pd.cut(self.df['year'], bins=bins, labels=labels)

        # 6. Medal numeric mapping (useful for sorting)
        medal_map = {'Gold': 1, 'Silver': 2, 'Bronze': 3}
        self.df['medal_rank'] = self.df['medal'].map(medal_map)

        after = len(self.df)
        print(f"[DataLoader] ✅ Cleaned. Rows before: {before:,} | After: {after:,}")
        print(f"[DataLoader] Added columns: 'bmi', 'era', 'medal_rank'")
        return self

    def merge_country_info(self):
        """Merge main data with country reference data."""
        self.df = self.df.merge(self.country_df, on='noc', how='left')
        print("[DataLoader] ✅ Merged country info (region, population)")
        return self

    def get_data(self):
        """Return the cleaned DataFrame."""
        return self.df

    def summary(self):
        """Print a quick summary of the loaded dataset."""
        print(f"\n{'─'*40}")
        print(f"  DATASET SUMMARY")
        print(f"{'─'*40}")
        print(f"  Total records  : {len(self.df):,}")
        print(f"  Years covered  : {self.df['year'].min()} – {self.df['year'].max()}")
        print(f"  Sports         : {self.df['sport'].nunique()}")
        print(f"  Countries (NOC): {self.df['noc'].nunique()}")
        print(f"  Athletes (est) : {self.df['athlete_id'].nunique():,}")
        print(f"  Total medals   : {len(self.df):,}")
        print(f"{'─'*40}")


# Using the class (this is how OOP is used)
loader = OlympicsDataLoader(path("olympics_data.csv"), path("country_info.csv"))
loader.load().clean().merge_country_info()   # Method chaining
loader.summary()
df = loader.get_data()  # Get the cleaned, enriched DataFrame


# ╔══════════════════════════════════════════════════════════╗
# ║  MODULE 3 — MEDAL TALLY & COUNTRY ANALYSIS (Intermediate)║
# ╚══════════════════════════════════════════════════════════╝
"""
LEARNING GOALS:
- pandas groupby, pivot_table, crosstab
- Sorting, ranking, filtering
- Inheritance in OOP
- Matplotlib bar charts, pie charts, heatmaps
"""

print("\n" + "─" * 60)
print("  MODULE 3: MEDAL TALLY & COUNTRY ANALYSIS")
print("─" * 60)


class MedalAnalyzer:
    """
    Analyzes medal data at country level.
    
    OOP CONCEPT: Composition
    - MedalAnalyzer takes a DataFrame and works on it
    - Keeps medal logic separate from data loading logic
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def get_overall_tally(self, top_n: int = 15) -> pd.DataFrame:
        """
        Get overall medal tally across all Olympic Games.
        Returns a DataFrame with Gold, Silver, Bronze counts.
        """
        # groupby + unstack — a very common pandas pattern
        tally = (
            self.df.groupby(['team', 'medal'])
            .size()
            .unstack(fill_value=0)  # Pivot medal types to columns
        )

        # Make sure all three columns exist
        for medal in ['Gold', 'Silver', 'Bronze']:
            if medal not in tally.columns:
                tally[medal] = 0

        tally['Total'] = tally['Gold'] + tally['Silver'] + tally['Bronze']

        # Sort by Gold first, then Silver (like official Olympic rankings)
        tally = tally.sort_values(['Gold', 'Silver', 'Bronze'], ascending=False)
        tally['Rank'] = range(1, len(tally) + 1)

        return tally[['Rank', 'Gold', 'Silver', 'Bronze', 'Total']].head(top_n)

    def get_tally_by_year(self, country: str) -> pd.DataFrame:
        """Get medal tally for a specific country across years."""
        country_df = self.df[self.df['team'] == country]
        yearly = (
            country_df.groupby(['year', 'medal'])
            .size()
            .unstack(fill_value=0)
        )
        for medal in ['Gold', 'Silver', 'Bronze']:
            if medal not in yearly.columns:
                yearly[medal] = 0
        yearly['Total'] = yearly[['Gold', 'Silver', 'Bronze']].sum(axis=1)
        return yearly

    def get_region_performance(self) -> pd.DataFrame:
        """Medal performance by geographic region."""
        return (
            self.df.groupby('region')['medal']
            .value_counts()
            .unstack(fill_value=0)
        )

    def plot_top_countries(self, top_n: int = 10):
        """Stacked bar chart of top countries by medal count."""
        tally = self.get_overall_tally(top_n)

        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        fig.suptitle(f'Top {top_n} Countries — Olympic Medal Performance',
                     fontsize=14, fontweight='bold', y=1.02)

        # ── Chart 1: Stacked bar chart ───────────────────────
        countries_list = tally.index.tolist()
        gold_vals = tally['Gold'].values
        silver_vals = tally['Silver'].values
        bronze_vals = tally['Bronze'].values
        x = np.arange(len(countries_list))
        width = 0.5

        axes[0].bar(x, gold_vals, width, label='Gold', color='#FFD700')
        axes[0].bar(x, silver_vals, width, bottom=gold_vals, label='Silver', color='#C0C0C0')
        axes[0].bar(x, bronze_vals, width,
                    bottom=gold_vals + silver_vals, label='Bronze', color='#CD7F32')

        axes[0].set_xticks(x)
        axes[0].set_xticklabels(countries_list, rotation=45, ha='right', fontsize=9)
        axes[0].set_title('Stacked Medal Count by Country')
        axes[0].set_ylabel('Number of Medals')
        axes[0].legend()
        axes[0].grid(axis='y', alpha=0.3)

        # ── Chart 2: Horizontal bar (Gold medals only) ───────
        axes[1].barh(countries_list, gold_vals, color='#FFD700', edgecolor='black', linewidth=0.5)
        axes[1].set_title('Gold Medals Only (Ranking)')
        axes[1].set_xlabel('Gold Medals')
        axes[1].invert_yaxis()  # Top country at the top
        axes[1].grid(axis='x', alpha=0.3)

        # Add value labels
        for i, v in enumerate(gold_vals):
            axes[1].text(v + 0.5, i, str(v), va='center', fontsize=8)

        plt.tight_layout()
        plt.savefig(path("output_charts/01_top_countries_medals.png"), dpi=150, bbox_inches='tight')
        plt.close()
        print("  ✅ Chart saved: output_charts/01_top_countries_medals.png")

    def plot_region_breakdown(self):
        """Pie chart and bar chart of medals by region."""
        region_data = self.df.groupby('region')['medal'].count()

        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle('Olympic Medals by Geographic Region', fontsize=14, fontweight='bold')

        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c']

        # Pie chart
        axes[0].pie(region_data.values, labels=region_data.index,
                    autopct='%1.1f%%', colors=colors, startangle=140,
                    wedgeprops={'edgecolor': 'white', 'linewidth': 1.5})
        axes[0].set_title('Share of Total Medals by Region')

        # Bar chart
        axes[1].bar(region_data.index, region_data.values,
                    color=colors[:len(region_data)], edgecolor='black', linewidth=0.5)
        axes[1].set_title('Total Medals Won by Region')
        axes[1].set_ylabel('Medals')
        axes[1].set_xlabel('Region')
        axes[1].tick_params(axis='x', rotation=20)
        axes[1].grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig(path("output_charts/02_region_breakdown.png"), dpi=150, bbox_inches='tight')
        plt.close()
        print("  ✅ Chart saved: output_charts/02_region_breakdown.png")


# Run Module 3
print("\n📊 Running Medal Analysis...")
medal_analyzer = MedalAnalyzer(df)

print("\n🥇 Overall Medal Tally (Top 15):")
tally = medal_analyzer.get_overall_tally()
print(tally.to_string())

medal_analyzer.plot_top_countries(10)
medal_analyzer.plot_region_breakdown()


# ╔══════════════════════════════════════════════════════════╗
# ║  MODULE 4 — ATHLETE & SPORT ANALYTICS (Intermediate+)   ║
# ╚══════════════════════════════════════════════════════════╝
"""
LEARNING GOALS:
- Inheritance (SportAnalyzer extends BaseAnalyzer)
- Complex groupby with multiple aggregations
- Correlation analysis with NumPy
- Box plots, scatter plots, histograms
"""

print("\n" + "─" * 60)
print("  MODULE 4: ATHLETE & SPORT ANALYTICS")
print("─" * 60)


class BaseAnalyzer:
    """
    Base class with common utility methods.
    
    OOP CONCEPT: Inheritance
    - This is the PARENT class
    - Child classes will inherit these methods
    - Code reuse — don't repeat yourself (DRY principle)
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def filter_by_year_range(self, start: int, end: int) -> pd.DataFrame:
        """Filter data between two years."""
        return self.df[(self.df['year'] >= start) & (self.df['year'] <= end)]

    def filter_by_country(self, country: str) -> pd.DataFrame:
        """Filter data for a specific country name."""
        return self.df[self.df['team'] == country]

    def filter_by_sport(self, sport: str) -> pd.DataFrame:
        """Filter data for a specific sport."""
        return self.df[self.df['sport'] == sport]

    def top_n(self, column: str, n: int = 10) -> pd.Series:
        """Return top N value counts for a column."""
        return self.df[column].value_counts().head(n)


class AthleteAnalyzer(BaseAnalyzer):
    """
    Analyzes athletes — extends BaseAnalyzer.
    
    OOP CONCEPT: Inheritance + Method Overriding
    - Inherits filter methods from BaseAnalyzer
    - Adds athlete-specific analysis methods
    """

    def physical_stats_by_sport(self) -> pd.DataFrame:
        """
        Average physical attributes (age, height, weight, BMI) per sport.
        Uses .agg() for multiple aggregations at once — very powerful!
        """
        stats = self.df.groupby('sport').agg(
            avg_age=('age', 'mean'),
            avg_height=('height_cm', 'mean'),
            avg_weight=('weight_kg', 'mean'),
            avg_bmi=('bmi', 'mean'),
            total_medals=('medal', 'count')
        ).round(2)

        return stats.sort_values('total_medals', ascending=False)

    def age_distribution_by_medal(self):
        """Box plot — age distribution for each medal type."""
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle('Athlete Physical Profile Analysis', fontsize=14, fontweight='bold')

        # ── Box Plot: Age by Medal ──
        medal_order = ['Gold', 'Silver', 'Bronze']
        colors_box = ['#FFD700', '#C0C0C0', '#CD7F32']

        data_to_plot = [self.df[self.df['medal'] == m]['age'].dropna().values
                        for m in medal_order]

        bp = axes[0].boxplot(data_to_plot, labels=medal_order,
                             patch_artist=True, notch=False)
        for patch, color in zip(bp['boxes'], colors_box):
            patch.set_facecolor(color)
            patch.set_alpha(0.8)

        axes[0].set_title('Age Distribution by Medal Type')
        axes[0].set_ylabel('Age (years)')
        axes[0].grid(axis='y', alpha=0.3)

        # ── Histogram: Age distribution ─────────────────────
        axes[1].hist(self.df['age'].dropna(), bins=20, color='steelblue',
                     edgecolor='white', linewidth=0.5, alpha=0.85)
        axes[1].axvline(self.df['age'].mean(), color='red', linestyle='--',
                        linewidth=2, label=f"Mean: {self.df['age'].mean():.1f}")
        axes[1].axvline(self.df['age'].median(), color='orange', linestyle='--',
                        linewidth=2, label=f"Median: {self.df['age'].median():.1f}")
        axes[1].set_title('Overall Age Distribution of Medalists')
        axes[1].set_xlabel('Age')
        axes[1].set_ylabel('Count')
        axes[1].legend()
        axes[1].grid(alpha=0.3)

        plt.tight_layout()
        plt.savefig(path("output_charts/03_age_analysis.png"), dpi=150, bbox_inches='tight')
        plt.close()
        print("  ✅ Chart saved: output_charts/03_age_analysis.png")

    def gender_participation_over_years(self):
        """Line chart showing male vs female athletes over time."""
        gender_year = (
            self.df.groupby(['year', 'sex'])
            .size()
            .unstack(fill_value=0)
        )

        fig, ax = plt.subplots(figsize=(12, 5))

        ax.plot(gender_year.index, gender_year.get('M', 0),
                marker='o', color='steelblue', linewidth=2, label='Male', markersize=4)
        ax.plot(gender_year.index, gender_year.get('F', 0),
                marker='s', color='salmon', linewidth=2, label='Female', markersize=4)

        ax.fill_between(gender_year.index, gender_year.get('M', 0), alpha=0.1, color='steelblue')
        ax.fill_between(gender_year.index, gender_year.get('F', 0), alpha=0.1, color='salmon')

        ax.set_title('Male vs Female Medal Winners Across Olympic Games', fontsize=13, fontweight='bold')
        ax.set_xlabel('Year')
        ax.set_ylabel('Number of Medal Winners')
        ax.legend(fontsize=11)
        ax.grid(alpha=0.3)
        ax.set_xticks(gender_year.index[::3])
        ax.tick_params(axis='x', rotation=45)

        plt.tight_layout()
        plt.savefig(path("output_charts/04_gender_over_years.png"), dpi=150, bbox_inches='tight')
        plt.close()
        print("  ✅ Chart saved: output_charts/04_gender_over_years.png")

    def height_weight_scatter(self, sample_size: int = 2000):
        """Scatter plot: Height vs Weight, colored by medal."""
        sample = self.df.sample(min(sample_size, len(self.df)), random_state=42)

        fig, ax = plt.subplots(figsize=(10, 7))

        medal_colors = {'Gold': '#FFD700', 'Silver': '#AAAAAA', 'Bronze': '#CD7F32'}

        for medal, color in medal_colors.items():
            subset = sample[sample['medal'] == medal]
            ax.scatter(subset['height_cm'], subset['weight_kg'],
                       c=color, label=medal, alpha=0.6, s=25, edgecolors='none')

        ax.set_xlabel('Height (cm)', fontsize=11)
        ax.set_ylabel('Weight (kg)', fontsize=11)
        ax.set_title('Athlete Height vs Weight by Medal Type', fontsize=13, fontweight='bold')
        ax.legend(title='Medal', fontsize=10)
        ax.grid(alpha=0.3)

        # Add trend line using numpy polyfit (linear regression manually!)
        valid = sample[['height_cm', 'weight_kg']].dropna()
        z = np.polyfit(valid['height_cm'], valid['weight_kg'], 1)  # degree=1 means linear
        p = np.poly1d(z)
        x_line = np.linspace(valid['height_cm'].min(), valid['height_cm'].max(), 100)
        ax.plot(x_line, p(x_line), "r--", linewidth=2, label='Trend line')
        ax.legend()

        plt.tight_layout()
        plt.savefig(path("output_charts/05_height_weight_scatter.png"), dpi=150, bbox_inches='tight')
        plt.close()
        print("  ✅ Chart saved: output_charts/05_height_weight_scatter.png")

    def correlation_matrix(self):
        """
        Compute and visualize correlation between numeric features.
        Uses NumPy correlation (np.corrcoef) and matplotlib heatmap.
        """
        numeric_cols = ['age', 'height_cm', 'weight_kg', 'bmi', 'medal_rank']
        data = self.df[numeric_cols].dropna()

        # np.corrcoef computes the correlation coefficient matrix
        corr_matrix = np.corrcoef(data.T)  # Transpose so each row is a variable

        fig, ax = plt.subplots(figsize=(8, 6))

        # Draw the heatmap manually using imshow (no seaborn needed!)
        im = ax.imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1, aspect='auto')
        plt.colorbar(im, ax=ax, label='Correlation Coefficient')

        ax.set_xticks(range(len(numeric_cols)))
        ax.set_yticks(range(len(numeric_cols)))
        ax.set_xticklabels(numeric_cols, rotation=45, ha='right')
        ax.set_yticklabels(numeric_cols)

        # Annotate each cell with the correlation value
        for i in range(len(numeric_cols)):
            for j in range(len(numeric_cols)):
                ax.text(j, i, f"{corr_matrix[i, j]:.2f}",
                        ha='center', va='center', fontsize=10,
                        color='black' if abs(corr_matrix[i, j]) < 0.7 else 'white')

        ax.set_title('Correlation Matrix — Athlete Physical Attributes', fontsize=13, fontweight='bold')
        plt.tight_layout()
        plt.savefig(path("output_charts/06_correlation_matrix.png"), dpi=150, bbox_inches='tight')
        plt.close()
        print("  ✅ Chart saved: output_charts/06_correlation_matrix.png")


class SportAnalyzer(BaseAnalyzer):
    """
    Analyzes sports and events — extends BaseAnalyzer.
    
    OOP CONCEPT: Inheritance
    - Inherits all utility methods from BaseAnalyzer
    - Focuses on sport-specific analysis
    """

    def medals_by_sport(self) -> pd.DataFrame:
        """Total medals per sport, broken down by type."""
        return (
            self.df.groupby(['sport', 'medal'])
            .size()
            .unstack(fill_value=0)
            .assign(Total=lambda x: x.sum(axis=1))
            .sort_values('Total', ascending=False)
        )

    def dominant_sport_per_country(self, country: str) -> pd.DataFrame:
        """Which sports a country dominates (most gold medals in)."""
        country_data = self.filter_by_country(country)
        gold_only = country_data[country_data['medal'] == 'Gold']
        return (
            gold_only.groupby('sport')
            .size()
            .sort_values(ascending=False)
            .head(10)
            .reset_index(name='Gold Medals')
        )

    def plot_top_sports(self, top_n: int = 12):
        """Horizontal bar chart of most medals-rich sports."""
        sport_medals = self.df.groupby('sport').size().sort_values(ascending=False).head(top_n)

        fig, ax = plt.subplots(figsize=(10, 7))

        colors = plt.cm.viridis(np.linspace(0.2, 0.8, top_n))
        bars = ax.barh(sport_medals.index[::-1], sport_medals.values[::-1],
                       color=colors, edgecolor='white', linewidth=0.5)

        ax.set_title(f'Top {top_n} Sports by Total Medals Awarded', fontsize=13, fontweight='bold')
        ax.set_xlabel('Total Medals')
        ax.grid(axis='x', alpha=0.3)

        for bar, val in zip(bars, sport_medals.values[::-1]):
            ax.text(val + 10, bar.get_y() + bar.get_height() / 2,
                    str(val), va='center', fontsize=9)

        plt.tight_layout()
        plt.savefig(path("output_charts/07_top_sports.png"), dpi=150, bbox_inches='tight')
        plt.close()
        print("  ✅ Chart saved: output_charts/07_top_sports.png")


# Run Module 4
print("\n📊 Running Athlete & Sport Analysis...")
athlete_analyzer = AthleteAnalyzer(df)
sport_analyzer = SportAnalyzer(df)

print("\n📌 Physical Stats by Sport (Top 10 by medals):")
print(athlete_analyzer.physical_stats_by_sport().head(10).to_string())

athlete_analyzer.age_distribution_by_medal()
athlete_analyzer.gender_participation_over_years()
athlete_analyzer.height_weight_scatter()
athlete_analyzer.correlation_matrix()
sport_analyzer.plot_top_sports()

print("\n📌 Top Sports for USA (Gold Medals):")
print(sport_analyzer.dominant_sport_per_country('United States').to_string())


# ╔══════════════════════════════════════════════════════════╗
# ║  MODULE 5 — ADVANCED ANALYTICS & PIPELINE (Advanced)    ║
# ╚══════════════════════════════════════════════════════════╝
"""
LEARNING GOALS:
- Abstract base class concept (simulation)
- ETL Pipeline pattern (Extract, Transform, Load)
- Advanced numpy: percentile, rolling computations
- Complex multi-panel matplotlib figures
- Data-driven storytelling with annotations
- Efficiency metrics (medals per million population)
- Reporting / exporting results
"""

print("\n" + "─" * 60)
print("  MODULE 5: ADVANCED ANALYTICS & REPORTING PIPELINE")
print("─" * 60)


class AdvancedAnalytics(BaseAnalyzer):
    """
    Advanced analytical methods — extends BaseAnalyzer.
    
    OOP CONCEPTS: Inheritance + Complex state management
    
    This class represents the kind of analytics a Data Engineer
    would build for a business intelligence report.
    """

    def __init__(self, df: pd.DataFrame):
        super().__init__(df)  # Call parent __init__ — always do this!
        self._cache = {}       # Cache computed results to avoid recomputing

    def medals_per_million(self, top_n: int = 15) -> pd.DataFrame:
        """
        Efficiency metric: Gold medals per million population.
        Small countries (Jamaica, Hungary) often punch above their weight!
        
        This is a real data analyst insight metric.
        """
        country_gold = (
            self.df[self.df['medal'] == 'Gold']
            .groupby(['team', 'population'])
            .size()
            .reset_index(name='gold_medals')
        )

        country_gold['gold_per_million'] = (
            country_gold['gold_medals'] / (country_gold['population'] / 1_000_000)
        ).round(4)

        return country_gold.sort_values('gold_per_million', ascending=False).head(top_n)

    def compute_rolling_dominance(self, country: str, window: int = 3) -> pd.DataFrame:
        """
        Compute rolling average of medals won — shows momentum trends.
        
        'Rolling' means looking at a window of consecutive years.
        Example: window=3 means average of last 3 Olympics.
        """
        yearly = (
            self.df[self.df['team'] == country]
            .groupby('year')
            .size()
            .reset_index(name='medals')
        )

        yearly['rolling_avg'] = (
            yearly['medals'].rolling(window=window, min_periods=1).mean().round(2)
        )
        return yearly

    def era_analysis(self) -> pd.DataFrame:
        """
        Medal distribution across historical eras.
        Shows how dominance shifted through history.
        """
        era_country = (
            self.df.groupby(['era', 'team', 'medal'])
            .size()
            .unstack(fill_value=0)
        )
        for medal in ['Gold', 'Silver', 'Bronze']:
            if medal not in era_country.columns:
                era_country[medal] = 0

        era_country['Total'] = era_country[['Gold', 'Silver', 'Bronze']].sum(axis=1)
        era_country = era_country.reset_index()

        # Convert era category to string to avoid groupby issues
        era_country['era'] = era_country['era'].astype(str)

        # Top 3 countries per era
        top_per_era = (
            era_country
            .groupby('era', group_keys=False)
            .apply(lambda x: x.nlargest(3, 'Gold'))
            .reset_index(drop=True)
        )
        cols = [c for c in ['era', 'team', 'Gold', 'Silver', 'Bronze', 'Total'] if c in top_per_era.columns]
        return top_per_era[cols]

    def numpy_advanced_stats(self) -> dict:
        """
        Advanced NumPy statistical operations.
        
        These are the kinds of stats a Data Scientist or
        Senior Data Engineer would compute.
        """
        medals_by_year = self.df.groupby('year').size().values

        stats = {
            'total_editions': len(np.unique(self.df['year'].values)),
            'avg_medals_per_game': np.mean(medals_by_year),
            'std_medals_per_game': np.std(medals_by_year),
            'growth_rate_pct': (
                (medals_by_year[-1] - medals_by_year[0]) / medals_by_year[0] * 100
            ),
            # Z-score: how many standard deviations above/below mean
            'z_scores_years': dict(zip(
                self.df['year'].unique(),
                np.round((medals_by_year - np.mean(medals_by_year)) / np.std(medals_by_year), 2)
            )),
            # Percentile breakdown of medals per country
            'medal_count_percentiles': {
                'p25': np.percentile(self.df.groupby('team').size().values, 25),
                'p50': np.percentile(self.df.groupby('team').size().values, 50),
                'p75': np.percentile(self.df.groupby('team').size().values, 75),
                'p90': np.percentile(self.df.groupby('team').size().values, 90),
            }
        }
        return stats

    def plot_comprehensive_dashboard(self):
        """
        A multi-panel dashboard — the kind of output you'd present to stakeholders.
        Uses matplotlib GridSpec for complex layouts.
        """
        fig = plt.figure(figsize=(20, 14))
        fig.suptitle('Olympic Games — Comprehensive Analytics Dashboard',
                     fontsize=16, fontweight='bold', y=0.98)

        # GridSpec lets you create complex grid layouts
        gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.35)

        # ── Panel 1 (top-left wide): Medal growth over time ─
        ax1 = fig.add_subplot(gs[0, :2])
        yearly_medals = self.df.groupby('year').size()
        ax1.bar(yearly_medals.index, yearly_medals.values,
                color='steelblue', alpha=0.7, width=3)
        # Rolling average overlay
        rolling = yearly_medals.rolling(3, min_periods=1).mean()
        ax1.plot(yearly_medals.index, rolling.values,
                 color='red', linewidth=2.5, label='3-Game Rolling Avg')
        ax1.set_title('Total Medals Awarded Per Olympic Games', fontweight='bold')
        ax1.set_xlabel('Year')
        ax1.set_ylabel('Medals')
        ax1.legend()
        ax1.grid(alpha=0.3)

        # ── Panel 2 (top-right): Medal split pie ─────────────
        ax2 = fig.add_subplot(gs[0, 2])
        medal_counts = self.df['medal'].value_counts()
        ax2.pie(medal_counts, labels=medal_counts.index,
                colors=['#FFD700', '#C0C0C0', '#CD7F32'],
                autopct='%1.0f%%', startangle=90,
                wedgeprops={'edgecolor': 'white', 'linewidth': 2})
        ax2.set_title('Medal Type Distribution', fontweight='bold')

        # ── Panel 3 (middle-left): Top 8 countries bar ───────
        ax3 = fig.add_subplot(gs[1, :2])
        tally = MedalAnalyzer(self.df).get_overall_tally(8)
        x = np.arange(len(tally))
        w = 0.25
        ax3.bar(x - w, tally['Gold'], w, color='#FFD700', label='Gold')
        ax3.bar(x, tally['Silver'], w, color='#C0C0C0', label='Silver')
        ax3.bar(x + w, tally['Bronze'], w, color='#CD7F32', label='Bronze')
        ax3.set_xticks(x)
        ax3.set_xticklabels(tally.index, rotation=30, ha='right', fontsize=8)
        ax3.set_title('Top 8 Countries — Medal Breakdown', fontweight='bold')
        ax3.set_ylabel('Medals')
        ax3.legend(fontsize=8)
        ax3.grid(axis='y', alpha=0.3)

        # ── Panel 4 (middle-right): Age distribution ─────────
        ax4 = fig.add_subplot(gs[1, 2])
        gold_ages = self.df[self.df['medal'] == 'Gold']['age'].dropna()
        silver_ages = self.df[self.df['medal'] == 'Silver']['age'].dropna()
        bronze_ages = self.df[self.df['medal'] == 'Bronze']['age'].dropna()
        ax4.hist(gold_ages, bins=15, alpha=0.6, color='#FFD700', label='Gold')
        ax4.hist(silver_ages, bins=15, alpha=0.5, color='#C0C0C0', label='Silver')
        ax4.hist(bronze_ages, bins=15, alpha=0.4, color='#CD7F32', label='Bronze')
        ax4.set_title('Age Distribution by Medal', fontweight='bold')
        ax4.set_xlabel('Age')
        ax4.legend(fontsize=8)
        ax4.grid(alpha=0.3)

        # ── Panel 5 (bottom-left): Medals by sport top 8 ─────
        ax5 = fig.add_subplot(gs[2, 0])
        sport_counts = self.df.groupby('sport').size().sort_values(ascending=False).head(8)
        ax5.barh(sport_counts.index[::-1], sport_counts.values[::-1],
                 color=plt.cm.Set2(np.linspace(0, 1, 8)))
        ax5.set_title('Medals by Sport (Top 8)', fontweight='bold', fontsize=9)
        ax5.set_xlabel('Count', fontsize=8)
        ax5.tick_params(labelsize=7)
        ax5.grid(axis='x', alpha=0.3)

        # ── Panel 6 (bottom-middle): Gender split over eras ──
        ax6 = fig.add_subplot(gs[2, 1])
        era_gender = (
            self.df.groupby(['era', 'sex'])
            .size()
            .unstack(fill_value=0)
        )
        eras = [str(e) for e in era_gender.index]
        male = era_gender.get('M', pd.Series(0, index=era_gender.index)).values
        female = era_gender.get('F', pd.Series(0, index=era_gender.index)).values
        x_era = np.arange(len(eras))
        ax6.bar(x_era, male, 0.4, label='Male', color='steelblue', alpha=0.8)
        ax6.bar(x_era, female, 0.4, bottom=male, label='Female', color='salmon', alpha=0.8)
        ax6.set_xticks(x_era)
        ax6.set_xticklabels(eras, fontsize=6, rotation=15)
        ax6.set_title('Gender Split by Era', fontweight='bold', fontsize=9)
        ax6.set_ylabel('Medals', fontsize=8)
        ax6.legend(fontsize=7)
        ax6.grid(axis='y', alpha=0.3)

        # ── Panel 7 (bottom-right): Efficiency metric ────────
        ax7 = fig.add_subplot(gs[2, 2])
        eff = self.medals_per_million(10)
        ax7.barh(eff['team'][::-1], eff['gold_per_million'][::-1],
                 color='goldenrod', edgecolor='white')
        ax7.set_title('Gold/Million Pop (Top 10)', fontweight='bold', fontsize=9)
        ax7.set_xlabel('Gold per Million', fontsize=8)
        ax7.tick_params(labelsize=7)
        ax7.grid(axis='x', alpha=0.3)

        plt.savefig(path("output_charts/08_comprehensive_dashboard.png"),
                    dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
        print("  ✅ Chart saved: output_charts/08_comprehensive_dashboard.png")

    def plot_country_trend(self, countries: list):
        """
        Line chart showing medal trends for selected countries across Olympic history.
        Data storytelling — one of the most important skills in analytics.
        """
        fig, ax = plt.subplots(figsize=(14, 6))

        colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6']

        for i, country in enumerate(countries):
            data = self.compute_rolling_dominance(country, window=3)
            if len(data) > 0:
                color = colors[i % len(colors)]
                ax.plot(data['year'], data['medals'],
                        marker='o', markersize=4, linewidth=1.5,
                        alpha=0.4, color=color)
                ax.plot(data['year'], data['rolling_avg'],
                        linewidth=2.5, color=color, label=country)

        ax.set_title('Medal Count Trend — Rolling 3-Olympics Average', fontsize=13, fontweight='bold')
        ax.set_xlabel('Olympic Year')
        ax.set_ylabel('Medals Won')
        ax.legend(fontsize=10)
        ax.grid(alpha=0.3)
        ax.set_xticks(df['year'].unique()[::3])
        ax.tick_params(axis='x', rotation=45)

        # Annotate key events
        ax.axvline(1980, color='gray', linestyle=':', alpha=0.7)
        ax.text(1981, ax.get_ylim()[1] * 0.9, 'Moscow\nBoycott', fontsize=7, color='gray')
        ax.axvline(1984, color='gray', linestyle=':', alpha=0.7)
        ax.text(1985, ax.get_ylim()[1] * 0.9, 'LA\nBoycott', fontsize=7, color='gray')
        ax.axvline(1992, color='gray', linestyle=':', alpha=0.7)
        ax.text(1993, ax.get_ylim()[1] * 0.9, 'Post-\nUSSR', fontsize=7, color='gray')

        plt.tight_layout()
        plt.savefig(path("output_charts/09_country_trends.png"), dpi=150, bbox_inches='tight')
        plt.close()
        print("  ✅ Chart saved: output_charts/09_country_trends.png")


class OlympicsReportPipeline:
    """
    ETL-style reporting pipeline — the most advanced OOP pattern here.
    
    OOP CONCEPTS: Composition + Pipeline Design Pattern
    
    This is what a Data Engineer builds in production:
    - Extract: load data
    - Transform: analyze and compute metrics  
    - Load/Report: export results to files
    
    In real jobs, this would write to a database, S3 bucket, or dashboard.
    """

    def __init__(self, df: pd.DataFrame):
        # Composition: pipeline holds instances of analyzer classes
        self.df = df
        self.medal_analyzer = MedalAnalyzer(df)
        self.athlete_analyzer = AthleteAnalyzer(df)
        self.sport_analyzer = SportAnalyzer(df)
        self.advanced = AdvancedAnalytics(df)
        self._report = {}    # Will store all computed results

    def extract(self):
        """E in ETL: validate our data is ready."""
        print("\n[Pipeline] ── EXTRACT ──────────────────────────")
        assert len(self.df) > 0, "DataFrame is empty!"
        assert 'medal' in self.df.columns, "Missing 'medal' column"
        assert 'year' in self.df.columns, "Missing 'year' column"
        print(f"[Pipeline] ✅ Data validated: {len(self.df):,} records ready")
        return self

    def transform(self):
        """T in ETL: compute all metrics and analyses."""
        print("\n[Pipeline] ── TRANSFORM ────────────────────────")

        self._report['overall_tally'] = self.medal_analyzer.get_overall_tally(20)
        print("[Pipeline] ✅ Medal tally computed")

        self._report['physical_stats'] = self.athlete_analyzer.physical_stats_by_sport()
        print("[Pipeline] ✅ Physical stats computed")

        self._report['efficiency'] = self.advanced.medals_per_million(15)
        print("[Pipeline] ✅ Efficiency metrics computed")

        self._report['numpy_stats'] = self.advanced.numpy_advanced_stats()
        print("[Pipeline] ✅ Advanced numpy stats computed")

        self._report['era_analysis'] = self.advanced.era_analysis()
        print("[Pipeline] ✅ Era analysis computed")

        return self

    def load(self):
        """L in ETL: save all results to output files."""
        print("\n[Pipeline] ── LOAD ──────────────────────────────")

        # output_reports folder already created at startup

        # Save to Excel (multi-sheet) — very common in data engineering
        with pd.ExcelWriter(path("output_reports/olympics_analysis_report.xlsx"),
                            engine='openpyxl') as writer:
            self._report['overall_tally'].to_excel(writer, sheet_name='Medal Tally')
            self._report['physical_stats'].to_excel(writer, sheet_name='Physical Stats')
            self._report['efficiency'].to_excel(writer, sheet_name='Efficiency Metrics')
            self._report['era_analysis'].to_excel(writer, sheet_name='Era Analysis')

        print("[Pipeline] ✅ Excel report saved: output_reports/olympics_analysis_report.xlsx")

        # Save to CSV
        self._report['overall_tally'].to_csv(path("output_reports/medal_tally.csv"))
        self._report['efficiency'].to_csv(path("output_reports/efficiency_metrics.csv"), index=False)
        print("[Pipeline] ✅ CSV files saved to output_reports/")

        return self

    def generate_all_charts(self):
        """Generate all visualizations."""
        print("\n[Pipeline] ── CHARTS ───────────────────────────")
        self.medal_analyzer.plot_top_countries(10)
        self.medal_analyzer.plot_region_breakdown()
        self.athlete_analyzer.age_distribution_by_medal()
        self.athlete_analyzer.gender_participation_over_years()
        self.athlete_analyzer.height_weight_scatter()
        self.athlete_analyzer.correlation_matrix()
        self.sport_analyzer.plot_top_sports()
        self.advanced.plot_comprehensive_dashboard()
        self.advanced.plot_country_trend(
            ['United States', 'Great Britain', 'China', 'Australia', 'Germany']
        )
        print("[Pipeline] ✅ All 9 charts generated!")
        return self

    def run(self):
        """Run the complete pipeline end-to-end."""
        print("\n" + "=" * 55)
        print("  RUNNING FULL OLYMPICS ANALYTICS PIPELINE")
        print("=" * 55)
        return (self.extract()
                    .transform()
                    .generate_all_charts()
                    .load())

    def print_insights(self):
        """Print key insights from the analysis."""
        numpy_stats = self._report['numpy_stats']
        tally = self._report['overall_tally']
        eff = self._report['efficiency']

        print("\n" + "=" * 55)
        print("  📊 KEY INSIGHTS FROM ANALYSIS")
        print("=" * 55)
        print(f"\n🏅 Total Olympic Editions Analyzed : {numpy_stats['total_editions']}")
        print(f"🏅 Avg Medals per Games            : {numpy_stats['avg_medals_per_game']:.1f}")
        print(f"🏅 Std Dev Medals per Games        : {numpy_stats['std_medals_per_game']:.1f}")
        print(f"🏅 Medal Count Growth (first→last) : {numpy_stats['growth_rate_pct']:.1f}%")
        print(f"\n🥇 All-Time #1 Country            : {tally.index[0]} ({tally['Gold'].iloc[0]} golds)")
        print(f"🥇 All-Time #2 Country            : {tally.index[1]} ({tally['Gold'].iloc[1]} golds)")

        print(f"\n📈 Medal Count Percentiles (by country):")
        for k, v in numpy_stats['medal_count_percentiles'].items():
            print(f"   {k}: {v:.0f} medals")

        print(f"\n🏋️  Most Efficient Country (Gold/million pop):")
        top_eff = eff.iloc[0]
        print(f"   {top_eff['team']}: {top_eff['gold_per_million']:.4f} golds/million")
        print("\n" + "=" * 55)


# ── Run the Full Pipeline ────────────────────────────────────
pipeline = OlympicsReportPipeline(df)
pipeline.run()
pipeline.print_insights()

print("\n" + "=" * 60)
print("  ✅ PROJECT COMPLETE!")
print("=" * 60)
print("""
📁 OUTPUT FILES:
  output_charts/   → 9 visualisation PNG files
  output_reports/  → Excel report + CSV files

📚 WHAT YOU LEARNED:
  Module 1 → Loading CSVs, .head(), .dtypes, .describe()
  Module 2 → OOP basics: class, __init__, self, methods
  Module 3 → groupby, pivot, sorting, stacked bar charts
  Module 4 → Inheritance, .agg(), scatter, box plots, correlation
  Module 5 → Advanced OOP, ETL pipeline, rolling avg, numpy stats

💼 JOB-READY SKILLS DEMONSTRATED:
  ✓ Clean, modular, reusable code
  ✓ OOP design patterns (Composition, Inheritance, Encapsulation)
  ✓ Data cleaning pipeline
  ✓ Multi-sheet Excel reporting
  ✓ Business metrics (efficiency ratio, rolling trend)
  ✓ Stakeholder-ready dashboards
  ✓ NumPy statistical analysis
  ✓ End-to-end ETL pipeline design
""")
