import yfinance as yf
from yahoo_fin import stock_info as si
from mail_sender import send_mail

import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()

def test_print(data):
    print("\n\n Test \n\n", data, "\n\n\n")

class AlphaVantageAPI:

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"
        

    def get_stock_metrics_data(self, function, symbol):

        params = {
            "apikey": self.api_key,
            "function": function,
            "symbol": symbol,
        }

        response = requests.get(self.base_url, params=params)
        data = response.json()
        return data


class FinancialAnalysis:

    def __init__(self, ticker_symbol, start_date, end_date):
        self.ticker_symbol = ticker_symbol
        self.start_date = start_date
        self.end_date = end_date
        self.stock_data = None
        self.stock_info = None

    def retrieve_stock_data(self):
        # Retrieve historical stock data from Yahoo Finance API
        self.stock_data = yf.download(self.ticker_symbol, start=self.start_date, end=self.end_date)
        self.stock_info = yf.Ticker(self.ticker_symbol).info
        # print(f"\n Retrievied Stock Data for the {self.ticker_symbol} stock \n", self.stock_data)

    def calculate_metrics(self, total_market_cap):

        financial_reports = AlphaVantageAPI(os.environ['api_key'])
        company_overview = financial_reports.get_stock_metrics_data("OVERVIEW",self.ticker_symbol)
        income_statement = financial_reports.get_stock_metrics_data("INCOME_STATEMENT",self.ticker_symbol)
        cash_flow_statement = financial_reports.get_stock_metrics_data("CASH_FLOW", self.ticker_symbol)



        is_quarterly_reports = income_statement["quarterlyReports"]
        is_annual_reports = income_statement["annualReports"]
        cfs_annual_reports = cash_flow_statement["annualReports"]
        
        self.stock_data['Symbol'] = self.ticker_symbol

        # For S&P 500 weight (%)
        self.stock_data['SP500_Weight'] = round(self.stock_info['marketCap']*100/total_market_cap,2)

        # For Last close price ($)
        self.stock_data['Last_Close_Price'] = round(self.stock_data['Close'],2)

        # For Operating Margin (%)
        
        num_of_quarters = 4

        operating_margins = [float(is_quarterly_reports[i]['operatingIncome'])/float(is_quarterly_reports[i]['totalRevenue']) for i in range(0,num_of_quarters)]
        
        average_operating_margin = sum(operating_margins)/num_of_quarters
       
        self.stock_data['Operating_Margin'] = average_operating_margin * 100

        # For EV/(EBITDA - CapEx) metric

        this_year_ev_ebitda_ratio = float(company_overview['EVToEBITDA'])
        ebitda_last_year = int(is_annual_reports[0]['ebitda'])
        capital_expenditures = int(cfs_annual_reports[0]['capitalExpenditures'])

        self.stock_data['Company_Valuation_Performance'] = (this_year_ev_ebitda_ratio*ebitda_last_year)/(ebitda_last_year - capital_expenditures)

        # Calculate Stock YTD performance
        this_year = self.start_date.split('-')[0]
        year_start = f"{this_year}-01-01"
        year_end = f"{this_year}-01-07"
        stock_price_at_year_start = yf.download(self.ticker_symbol, start=year_start, end=year_end)['Close'][0]

        self.stock_data['Stock_YTD_Performance'] = (self.stock_data['Last_Close_Price'] - stock_price_at_year_start)*100/stock_price_at_year_start

        # Calculate Revenue - 1 year annualized growth (%)
        if(len(is_annual_reports)<=1): 
            self.stock_data['Revenue_Growth'] = 0
        else:
            self.stock_data['Revenue_Growth'] = (int(is_annual_reports[0]['totalRevenue']) - int(is_annual_reports[1]['totalRevenue']))*100.0/int(is_annual_reports[1]['totalRevenue'])

        # Calculate Net Income - 1 year annualized growth (%)

        if(len(is_annual_reports)<=1): 
            self.stock_data['Net_Income_Growth'] = 0
        else:
            self.stock_data['Net_Income_Growth'] = (int(is_annual_reports[0]['netIncome']) - int(is_annual_reports[1]['netIncome']))*100.0/int(is_annual_reports[1]['netIncome'])

        # # Calculate Short Interest (%)
        # self.stock_data['Short_Interest'] = (self.stock_data['ShortInterest'] / self.stock_data['SharesOutstanding']) * 100

    def get_metrics_data(self):
        # Return the calculated metrics data
        return self.stock_data[['Symbol','SP500_Weight', 'Last_Close_Price',  'Operating_Margin', 'Company_Valuation_Performance', 'Stock_YTD_Performance', 'Revenue_Growth', 'Net_Income_Growth']]



# Define the ticker symbols and date range
ticker_symbols = ["GOOG", "AMZN", "AAPL"]
start_date = "2023-05-19"
end_date = "2023-05-20"

# Create StockData objects for each ticker symbol
stock_data_objects = []

# table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
# df = table[0]

# sp_tickers = ["GOOG", "AMZN", "AAPL"] #[ticker for ticker in df['Symbol']]

# stocks_market_cap = []
# for ticker in sp_tickers:
#     try: 
#         stocks_market_cap.append(yf.Ticker(ticker).info["marketCap"])
#     except:
#         print('\nError with: ', ticker)


sp500index_market_cap =  38010268372736




for ticker_symbol in ticker_symbols:
    stock_data = FinancialAnalysis(ticker_symbol, start_date, end_date)
    stock_data.retrieve_stock_data()
    stock_data.calculate_metrics(sp500index_market_cap)
    stock_data_objects.append(stock_data)

# # Get and print the metrics data for each StockData object
df = pd.DataFrame()
for stock_data in stock_data_objects:
    metrics_data = stock_data.get_metrics_data()
    df = pd.concat([df,metrics_data], ignore_index=True)
    print('\n\n')

print(df, "\n", type(df))

df.to_excel(f"Financial Analysis - {start_date}.xlsx")


sender = "Kowshik Kumar"
date = start_date
file_path = f"Financial Analysis - {start_date}.xlsx"
subject = f"Financial Analysis for Stocks on {start_date}"
send_mail(sender, date, file_path)