from flask import Flask, Response
import pandas as pd
import os

app = Flask(__name__)

# Absolute path to the local file with an HTML table
FILE_PATH = r"C:\Users\avram\OneDrive\Desktop\Bloomtech TRG\TRG Week 42\bac.us.txt"


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
