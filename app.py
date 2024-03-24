from flask import Flask, jsonify
import tabula
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)

def get_previous_date():
   
    current_date = datetime.today()


    previous_date = current_date - timedelta(days=1)

    formatted_date = previous_date.strftime("%Y/%m/%d")
    formatted_date2 = previous_date.strftime("%Y-%m-%d")

    return formatted_date, formatted_date2

@app.route('/')
def scrape_pdf_and_return_json():
    previous_date, file_date = get_previous_date()


    pdf_url = "https://luse.co.zm/wp-content/uploads/" + previous_date + "-March-2024-Trade-Summary-Report.pdf"

   
    csv_file = file_date + "-trade_summary.csv"


    tables = tabula.read_pdf(pdf_url, pages="all", multiple_tables=True)
   
    df = pd.concat(tables)


    df.dropna(axis=0, how="all", inplace=True)


    df.reset_index(drop=True, inplace=True)

    
    df.to_csv(csv_file, index=False)

    json_data = df.to_dict(orient='records')

    return jsonify(json_data)

if __name__ == '__main__':
    app.run(debug=True)
