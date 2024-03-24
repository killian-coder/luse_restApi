import sys
import requests
import tabula
import pandas as pd
from datetime import datetime, timedelta

def get_today_date():
  
    current_date = datetime.today()
    
    formatted_date = current_date.strftime("%Y/%m/%d")
    formatted_date2 = current_date.strftime("%Y-%m-%d")

    return formatted_date, formatted_date2

# Get today's date
today_date, file_date = get_today_date()
log_message = f"Today's date (YYYY/MM/DD): {today_date}\n"
print(log_message)

# Construct PDF URL using today's date
pdf_url = "https://luse.co.zm/wp-content/uploads/" + today_date + "-March-2024-Trade-Summary-Report.pdf"
log_message = f"PDF URL: {pdf_url}\n"
print(log_message)

# Check if the PDF URL returns a 404 status code
response = requests.head(pdf_url)
if response.status_code == 404:
    log_message = today_date + " PDF URL returned 404 Not Found.\n"
    print(log_message)
    with open("logfile.txt", "a") as f:
        f.write(log_message)
    sys.exit("Error: PDF URL returned 404 Not Found. Exiting script.")
else:
    
    csv_file = "trade_data/"+file_date + "-trade_summary.csv"

    tables = tabula.read_pdf(pdf_url, pages="all", multiple_tables=True)
    log_message = "Tables extracted from PDF.\n"
    print(log_message)

    df = pd.concat(tables)

    df.dropna(axis=0, how="all", inplace=True)

    df.reset_index(drop=True, inplace=True)

    df.to_csv(csv_file, index=False)

    log_message = f"Data successfully scraped and saved to {csv_file}\n"
    print(log_message)

    with open("logfile.txt", "a") as f:
        f.write(log_message)
