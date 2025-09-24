from flask import Flask, Response
import pandas as pd
import os

app = Flask(__name__)

# Absolute path to the local file with an HTML table
FILE_PATH = r"C:\Users\avram\OneDrive\Desktop\Bloomtech TRG\TRG Week 42\bac.us.txt"

# Module-level DataFrames (populated on first load)
df_full = None
df_early = None
df_mid = None
df_late = None



def load_first_table_html(path):
    """Load the first HTML table from the given file path and return HTML string.

    Returns a tuple (html_string, error). html_string is the rendered HTML when successful.
    """
    if not os.path.exists(path):
        return None, f"file not found: {path}"

    html_error = None
    # First attempt: parse as HTML tables
    try:
        tables = pd.read_html(path)
        if tables:
            df = tables[0]
            # ensure Date is datetime
            if "Date" in df.columns:
                df["Date"] = pd.to_datetime(df["Date"])
            # Remove OpenInt column if present
            if "OpenInt" in df.columns:
                df = df.drop(columns=["OpenInt"])
            # populate module-level DataFrames for further analysis
            _populate_splits(df)
            table_html = df.to_html(index=False)
            full_html = (
                "<html><head><meta charset='utf-8'><title>bac.us table</title>"
                "</head><body>" + table_html + "</body></html>"
            )
            return full_html, None
    except Exception as e:
        html_error = str(e)

    # Fallback: parse as CSV (the provided file appears to be CSV)
    try:
        df = pd.read_csv(path)
        # parse Date column
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"])
        # Remove OpenInt column if present
        if "OpenInt" in df.columns:
            df = df.drop(columns=["OpenInt"])
        # populate module-level DataFrames for further analysis
        _populate_splits(df)
        table_html = df.to_html(index=False)
        full_html = (
            "<html><head><meta charset='utf-8'><title>bac.us table</title>"
            "</head><body>" + table_html + "</body></html>"
        )
        return full_html, None
    except Exception as e2:
        # Report both failures when available
        if html_error:
            return None, f"read_html error: {html_error}; read_csv error: {e2}"
        return None, str(e2)


@app.route("/")
def index():
    """Return the first table as an HTML page. HTML-only endpoint (no JSON)."""
    html, err = load_first_table_html(FILE_PATH)
    if err:
        return Response(f"Error loading table: {err}", status=500, mimetype="text/plain")
    # Return the HTML table directly
    return Response(html, mimetype="text/html")


if __name__ == "__main__":
    # Run the app on localhost:5000
    app.run(host="127.0.0.1", port=5000, debug=True)


def _populate_splits(df: pd.DataFrame):
    """Populate module-level DataFrames: df_full, df_early, df_mid, df_late.

    Split logic (chosen by judgment):
    - df_early: 1986-05-29 through 1999-12-31 (long-run historical period)
    - df_mid: 2000-01-01 through 2008-12-31 (pre/post-dotcom through financial crisis)
    - df_late: 2009-01-01 through 2017-11-10 (post-crisis recovery)
    """
    global df_full, df_early, df_mid, df_late
    df_full = df.copy()
    # Ensure Date exists and is datetime
    if "Date" not in df_full.columns:
        # if no Date column, leave splits as None
        df_early = df_mid = df_late = None
        return

    # Define cutoffs
    early_end = pd.Timestamp("1999-12-31")
    mid_start = pd.Timestamp("2000-01-01")
    mid_end = pd.Timestamp("2008-12-31")
    late_start = pd.Timestamp("2009-01-01")

    df_early = df_full[df_full["Date"] <= early_end].reset_index(drop=True)
    df_mid = df_full[(df_full["Date"] >= mid_start) & (df_full["Date"] <= mid_end)].reset_index(drop=True)
    df_late = df_full[df_full["Date"] >= late_start].reset_index(drop=True)

