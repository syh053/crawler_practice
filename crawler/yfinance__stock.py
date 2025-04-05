#%%
import yfinance as yf
from datetime import datetime, timedelta

today = datetime.today()
older_day = datetime.today() - timedelta(days=55)

today_str = datetime.strftime(today , "%Y-%m-%d")
older_day_str = datetime.strftime(older_day , "%Y-%m-%d")

print(today_str)
print(older_day_str)

# 取 30 筆資料
data = yf.Ticker("^TWII").history(start = older_day_str, end = today_str)[:30]

# 取需要的欄位
data = data[["Open", "High", "Low", "Close", "Volume"]]

# 將數據都調整為小數點後 2 位
# data["Close"] = data["Close"].apply(lambda x : float(f"{x:.2f}")) # 等同於下面作法
data["Open"] = data["Open"].round(2)
data["High"] = data["High"].round(2)
data["Low"] = data["Low"].round(2)
data["Close"] = data["Close"].round(2)

# 將成交量轉以 "億" 為單位並取小數點後 2 位
data["Volume"] = (data["Volume"] / 1000).round(2) 

# 建立 sma5 技術線
data["SMA5"] = data["Close"].rolling(window=5).mean()

# 建立 sma5 技術線
data["SMA10"] = data["Close"].rolling(window=10).mean()

# 建立 sma5 技術線
data["SMA20"] = data["Close"].rolling(window=20).mean()


# print(len(data))
print(data)
