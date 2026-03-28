# Job Listings Scraper

A simple Python scraper that pulls job listings from the Real Python fake jobs site and saves the results to a CSV file.

## What This Program Does

- Sends a request to `https://realpython.github.io/fake-jobs/`
- Parses the HTML with Beautiful Soup
- Extracts job title, company, location, apply link, learn link, post date, and run date
- Saves the scraped data to `data/job_listing_data.csv`
- Saves run status and errors to `data/logs.json`

## Requirements

- Python 3
- The packages listed in `requirements.txt`

## Installation

1. Open a terminal in the project folder.
2. Create and activate a virtual environment.
3. Install the dependencies.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## How To Use The Program

Run the scraper from the project root:

```bash
python3 scraper.py
```

After the script finishes, check these files:

- `data/job_listing_data.csv`: scraped job listing data
- `data/logs.json`: run status, timestamps, row count, and any errors

## Output Columns

The CSV file contains these columns:

- `JOB_TITLE`
- `COMPANY_NAME`
- `LOCATION`
- `APPLY_LINK`
- `LEARN_LINK`
- `POST_DATE`
- `RUN_DATE`

## Notes

- The current source URL is hardcoded in `scraper.py`.
- Running the script again overwrites `data/job_listing_data.csv` and `data/logs.json`.
- The example site currently returns 100 job listings, so the CSV usually contains 100 rows plus the header row.

## Project Files

- `scraper.py`: main scraper script
- `requirements.txt`: Python dependencies
- `data/job_listing_data.csv`: scraped output data
- `data/logs.json`: run log file
