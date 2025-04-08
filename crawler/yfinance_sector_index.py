#%%
from pathlib import Path
import sys

# 設定 project_root
project_root = Path(__file__).resolve().parent.parent

sys.path.append(str(project_root))


import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import yfinance as yf
from mysql_data.create_database_20250331 import cursor, conn


# yahoo 類股指數
url = "https://tw.stock.yahoo.com/sector-index"

# 設定 headers
headers = {
  "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

# 發出 GET 請求
responese = requests.get(url, headers = headers).text

soup = BeautifulSoup(responese, "lxml")

table = soup.find(class_ = "D(g) Gtc(fourEvenItems) Gtc(threeEvenItems)--narrow Colmg(20px) Rowg(32px) Gp(32px)--wide")

datas = table.find_all("a")

# 建立正規表達式規則
pattern = r"/quote/([\^\w.^]+)"

sectors = {}

for data in datas :
  """ 利用正規表達式取得類股代碼 """ 
  result = re.search(pattern, data.get("href"))

  name = data.find(class_ = "C($c-button) Fw(700) Fz(16px)").text

  num = result.group(1)

  num = 'CHI' if num == '^NTCHI' else num

  num = 'BIM' if num == '^NTBIOI' else num

  num = 'SEC.TW' if num == '^NTSEMI' else num

  num = 'CPE.TW' if num == '^NTPCI' else num
  
  num = 'OPE' if num == '^NTOPTI' else num

  num = 'COI' if num == '^NTTELI' else num

  num = 'EPC' if num == '^NTECI' else num

  num = 'EPD' if num == '^NTECHI' else num

  num = 'INS' if num == '^NTESEI' else num

  num = 'OTE' if num == '^NTOTHI' else num

  num = 'OGE' if num == '^NTOILI' else num
    
  sectors[name] = num

# print(sectors)


""" 建立起始和結束日期 """
today = datetime.today() 

# 結束日期
start = datetime.strftime(today + timedelta(days = 1), "%Y-%m-%d")

#起始日期
end = datetime.strftime(today - timedelta(days = 150), "%Y-%m-%d")

""" 逐一取得類股指數 """
for name, code in sectors.items() :
  # 取得資料
  data = yf.Ticker(code).history(start = end, end = start)

  # 只取數據長度超過 20 筆的資料
  if len(data) > 20 :

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

    # 取 30 筆資料
    data = data[-30 :]


    """ 檢查資料庫是否有相同資料 """
    for index, value in data.iterrows():
      # 查詢指令
      sql = "SELECT * FROM analysis_datas WHERE name = %s AND date =%s"

      params = (name, index)

      cursor.execute(sql, params)

      datas = cursor.fetchall()

      if not datas :
        # 建立資料語句
        sql = """
          INSERT INTO analysis_datas (name, date, open, high, low, close, volume, sma5, sma10, sma20)
          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # 設定存入的參數
        params = (name, index, value['Open'], value['High'], value['Low'], value['Close'], value['Volume'], value['SMA5'], value['SMA10'], value['SMA20'])

        # 執行 SQL 語句
        cursor.execute(sql, params)

        conn.commit()

      else :
        print(f"{ name }_{ index } 資料已存在!")


