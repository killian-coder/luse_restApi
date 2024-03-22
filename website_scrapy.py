import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import tabula
import pandas as pd

# Function to fetch the PDF URL for yesterday's trade summary
def get_yesterday_trade_summary_url():
    yesterday = datetime.today() - timedelta(days=1)
    yesterday_str = yesterday.strftime("%d-%B-%Y")
    
    url = "https://luse.co.zm/market-data/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        # Find the trade summaries section
        trade_summaries_section = soup.find("div", class_="trade-summary")
        if trade_summaries_section:
            # Find all links in the trade summaries section
            summary_links = trade_summaries_section.find_all("a")
            print(summary_links)
            # Check each link for yesterday's date
            for link in summary_links:
                if yesterday_str in link.text:
                    pdf_url = link.get("href")
                    return pdf_url
    return None

# Function to convert PDF to CSV
def pdf_to_csv(pdf_url, output_csv):
    # Extract tables from the PDF file
    tables = tabula.read_pdf(pdf_url, pages="all", multiple_tables=True)
    # Combine all tables into a single DataFrame
    df = pd.concat(tables)
    # Remove rows with all NaN values
    df.dropna(axis=0, how="all", inplace=True)
    # Reset the index
    df.reset_index(drop=True, inplace=True)
    # Write the DataFrame to a CSV file
    df.to_csv(output_csv, index=False)

# Main function
def main():
    # Fetch URL of yesterday's trade summary PDF
    pdf_url = get_yesterday_trade_summary_url()
    if pdf_url:
        print("Found PDF URL:", pdf_url)
        # Convert PDF to CSV
        output_csv = "trade_summary.csv"
        pdf_to_csv(pdf_url, output_csv)
        print("Data successfully converted and saved to", output_csv)
    else:
        print("Trade summary PDF for yesterday not found.")

if __name__ == "__main__":
    main()
