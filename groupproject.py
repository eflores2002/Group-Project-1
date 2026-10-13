import pandas as pd
import yfinance as yf

print("Group Stock Analysis")

stocks = ["AMZN", "SBUX", "CMG"]

start_date = "2024-07-01"
end_date= "2025-07-01"

print("Stocks:", stocks)
print("Start Date:", start_date)
print("End Date:", end_date)

#Work Item 2-Downlaod Stock Data

print("\nWork Item 2 - Stock Data")

#Download stock data using yfinance
data = yf.download(
    stocks,
    start=start_date,
    end=end_date,
    auto_adjust=True,
    group_by="Column",
    progress=False
)

#Make sure the download worked
if data.empty:
    raise ValueError("No stock data was downloaded.")

#Show info about data
print("\nFirst 5 Rows:")
print(data.head())

print("\nLast 5 Rows:")
print(data.tail())

print("\nDate Range:")
print(data.index.min())
print(data.index.max())

print("\nNumber of Records:")
print(len(data))

print("\nColumn Names:")
print(data.columns)

print("\nData Types:")
print(data.dtypes)

print("\nMissing Values:")
print(data.isnull().sum())

