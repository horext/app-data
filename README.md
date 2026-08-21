# Horext Public Updater

## Seed CSV format

Files in `seeds/` use one consistent CSV format:

- UTF-8 without a byte-order mark (BOM)
- comma delimiter
- RFC 4180 quoting (`""` represents a quote inside a quoted value)
- one unique, non-empty name for every column
- a final newline; LF and CRLF line endings are both accepted

Text containing commas, quotes, or newlines must be quoted according to CSV rules. Generate or edit these files with a CSV-aware tool; do not construct rows by joining values with commas.
