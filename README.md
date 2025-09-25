# TRG Week 42

## $BAC (Bank of America)

-  A large U.S. multinational bank offering consumer & commercial banking, investment services, and wealth/asset management.

- https://www.kaggle.com/borismarjanovic/datasets

### 1st Commit

 - Added a small Flask API (`app/data.py`) that loads the table from `bac.us.txt` and serves it as HTML at `/` (tries HTML tables first, falls back to CSV parsing).

### 2nd Commit

 - Removed the `OpenInt` column from the dataframe during load (not needed for the planned analysis).
 - Split the data by date into three DataFrame objects for analysis:
	 - `df_early`: 1986-05-29 through 1999-12-31 — long-run historical period for baseline behavior.
	 - `df_mid`: 2000-01-01 through 2008-12-31 — includes the dot-com era and the run-up to the 2008 financial crisis.
	 - `df_late`: 2009-01-01 through 2017-11-10 — post-crisis recovery and modern market regime.
  
	Reasoning: these splits reflect recognizable market/regime boundaries (pre-2000, crisis era, and post-crisis recovery). They provide balanced periods for comparative analysis while keeping natural economic boundaries intact.

### 3rd Commit

 - Added `/monthly-avg` route that returns a PNG plot of monthly average 'Open' price for `df_early`, `df_mid`, and `df_late`.

### 4th Commit

 - Added `/monthly-range` route that returns a PNG plot of monthly High-Low range (max High - min Low) for `df_early`, `df_mid`, and `df_late`.

### 5th Commit

 - Added `/max-drawdown` route that returns a PNG comparing maximum drawdown (MDD) across `df_early`, `df_mid`, and `df_late`. MDD is used because it highlights historical downside risk and is directly comparable across regimes.

### Summary:

- Implemented a local Flask API (`app/data.py`) that loads `bac.us.txt` (HTML-first, CSV fallback), drops `OpenInt`, parses dates, and creates three period splits (1986–1999, 2000–2008, 2009–2017). It exposes visualization endpoints: `/` (table), `/monthly-avg`, `/monthly-range`, and `/max-drawdown` (PNG outputs) to inspect monthly average open, monthly high-low range, and maximum drawdown per period.
- Reasoning: the period splits align with distinct market/regime phases so comparisons are meaningful; the chosen metrics capture central tendency (monthly average), intra-month variability (high-low range), and historical downside risk (max drawdown), which together give a compact, actionable view for analysis and trader-focused risk assessment.