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

### 4th Commit

### 5th Commit

### Summary:

- Implemented a Flask API (`app/data.py`) that serves the `bac.us.txt` table as HTML at `/`, with a CSV fallback when HTML tables aren't present. The loader drops `OpenInt` and exposes three period splits (`df_early`, `df_mid`, `df_late`) for downstream analysis.
- Rationale: splitting by economic/regime periods (1986–1999, 2000–2008, 2009–2017) helps compare market behavior across structurally different regimes (pre-dotcom, crisis, post-crisis).