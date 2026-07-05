# Automated Sales Report Pipeline

A complete automation pipeline that scrapes live product data, cleans it, updates a Google Sheet, and emails a summary report — all with one script run.

## What this project does
- Scrapes live product listings (name, price, review count) from an e-commerce site
- Cleans and converts price/review data into usable numeric formats
- Pushes the cleaned dataset directly into a Google Sheet
- Automatically emails a summary report (total products, average price, top performers)

## Tools used
Python, requests, BeautifulSoup, pandas, gspread (Google Sheets API), yagmail

## Files
- `project3_full_pipeline.py` — full pipeline script
- `laptop_sales_cleaned.csv` — sample cleaned output

## Note
Credential files (.env, sheets_credentials.json) are excluded for security — see .gitignore
