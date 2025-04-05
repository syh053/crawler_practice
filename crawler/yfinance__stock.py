#%%
import sys
from pathlib import Path

# 設定 project_root
project_root = Path(__file__).resolve().parent.parent

sys.path.append(str(project_root))


import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from mysql_data.create_database_20250331 import conn, cursor

today = datetime.today()
older_day = datetime.today() - timedelta(days=55)

today_str = datetime.strftime(today , "%Y-%m-%d")
older_day_str = datetime.strftime(older_day , "%Y-%m-%d")

print(today_str)
print(older_day_str)

stock_name = "TWSE"

# 取 30 筆資料
data = yf.Ticker("^TWII").history(start = older_day_str, end = today_str)[-30 :]

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
data["SMA5"] = data["Close"].rolling(window=5).mean().round(2)

# 建立 sma5 技術線
data["SMA10"] = data["Close"].rolling(window=10).mean().round(2)

# 建立 sma5 技術線
data["SMA20"] = data["Close"].rolling(window=20).mean().round(2)

data["SMA5"] = data["SMA5"].fillna(0)
data["SMA10"] = data["SMA10"].fillna(0)
data["SMA20"] = data["SMA20"].fillna(0)


for index, value in data.iterrows():
  # SQL 查詢語句
  sql = """
    SELECT * FROM analysis_datas WHERE name = %s AND date = %s
  """

  params = (stock_name, index)

  # 執行查詢語句
  cursor.execute(sql, params)

  datas = cursor.fetchall()

  if not datas :
    # 建立資料語句
    sql = """
      INSERT INTO analysis_datas (name, date, open, high, low, close, volume, sma5, sma10, sma20)
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """


    # 設定存入的參數
    params = (stock_name, index, value['Open'], value['High'], value['Low'], value['Close'], value['Volume'], value['SMA5'], value['SMA10'], value['SMA20'])

    # 執行 SQL 語句
    cursor.execute(sql, params)

    conn.commit()

  else :
    print(f"{ stock_name }_{ index } 資料已存在!")


# print(len(data))
print(data)
