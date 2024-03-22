import tabula
import pandas as pd

from datetime import datetime, timedelta

def get_previous_date():
    # Get current date
    current_date = datetime.today()

    # Subtract one day
    previous_date = current_date - timedelta(days=1)

    # Format the date as "YYYY/MM/DD"
    formatted_date = previous_date.strftime("%Y/%m/%d")
    formatted_date2 = previous_date.strftime("%Y-%m-%d")

    return formatted_date, formatted_date2

# Test the function
previous_date,file_date = get_previous_date()
print("Previous date (YYYY/MM/DD):", previous_date)


# URL of the PDF file
pdf_url = "https://luse.co.zm/wp-content/uploads/"+previous_date+"-March-2024-Trade-Summary-Report.pdf"
print(pdf_url)

# Path to save CSV file
csv_file = file_date+"-trade_summary.csv"

# Extract tables from the PDF file
tables = tabula.read_pdf(pdf_url, pages="all", multiple_tables=True)

# Combine all tables into a single DataFrame
df = pd.concat(tables)

# Remove rows with all NaN values
df.dropna(axis=0, how="all", inplace=True)

# Reset the index
df.reset_index(drop=True, inplace=True)

# Write the DataFrame to a CSV file
df.to_csv(csv_file, index=False)

print("Data successfully scraped and saved to", csv_file)
