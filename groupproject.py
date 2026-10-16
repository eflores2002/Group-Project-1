import os
import pandas as pd
import yfinance as yf

os.makedirs("results", exist_ok=True)

print("Group Stock Analysis")

stocks = ["AMZN", "SBUX", "CMG"]

start_date = "2024-07-01"
end_date = "2025-07-01"

print("Stocks:", stocks)
print("Start Date:", start_date)
print("End Date:", end_date)

#Work Item 2 - Download Stock Data

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

#Get closing prices and trading volume
#Different yfinance versions stack the column levels in different orders, so check first
if "Close" not in data.columns.get_level_values(0):
    data = data.swaplevel(axis=1)

close_prices = data["Close"][stocks].copy()
volume = data["Volume"][stocks].copy()

#Remove dates where a closing price is missing
close_prices = close_prices.dropna()

#keep volume on the same dates
volume = volume.loc[close_prices.index]

print("\nRecords After Cleaning")
print(len(close_prices))

#Save the closing prices
close_prices.to_csv("results/closing_prices.csv")

#Work Item 3: Daily return and statistics
print("\nWork Item 3: Statistics")

#Calculate the daily percentage returns
daily_returns = close_prices.pct_change(fill_method=None) * 100

#Remove the first row
daily_returns = daily_returns.dropna()

print("\nDaily Percentage Returns:")
print(daily_returns.head())

#Calculate six stats for closing prices
price_stats = close_prices.agg([
    "count",
    "mean",
    "median",
    "min",
    "max",
    "std"
])

print("\nClosing Price Statistics:")
print(price_stats.round(2))

#Calculate the same stats for daily returns
return_stats = daily_returns.agg([
    "count",
    "mean",
    "median",
    "min",
    "max",
    "std"
])

print("\nDaily Return Statistics:")
print(return_stats.round(2))

#Calculate correlation between our three stocks
correlation = daily_returns.corr()

print("\nStock Correlation:")
print(correlation.round(2))

#Explain each pair of stocks
for i in range(len(stocks)):
    for j in range(i + 1, len(stocks)):
        stock1 = stocks[i]
        stock2 = stocks[j]
        number = correlation.loc[stock1, stock2]
        print("\n", stock1, "and", stock2,)
        print("Correlation:", round(number, 2))

        if number >= 0.7:
            print("These stocks have a strong positive relationship.")
        elif number >= 0.3:
            print("These stocks have a moderate positive relationship.")
        elif number <= -0.7:
            print("These stocks have a strong negative relationship.")
        else:
            print("These stocks have a weak linear relationship.")

#Save our results
daily_returns.to_csv("results/daily_returns.csv")
close_prices.to_csv("results/closing_prices.csv")

# Work Item 4 - monthly stuff
print("\nWork Item 4: Monthly Summary")

# avg closing price per month
monthly_avg_price = close_prices.resample("ME").mean()

print("\nMonthly Average Closing Price:")
print(monthly_avg_price.round(2))

# just peek at recent months
print("\nLast 6 Months:")
print(monthly_avg_price.tail(6))

# monthly avg of the daily returns
monthly_avg_return = daily_returns.resample("ME").mean()

print("\nMonthly Average Daily Return (%):")
print(monthly_avg_return.round(2))

# save
monthly_avg_price.to_csv("results/monthly_avg_price.csv")
monthly_avg_return.to_csv("results/monthly_avg_return.csv")