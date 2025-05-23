#%%
from pathlib import Path
import sys

# 設定 project_root
project_root = Path(__file__).resolve().parent.parent

sys.path.append(str(project_root))


import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
from datetime import datetime
import time

from mysql_data.create_database_20250331 import conn, cursor


# 記錄開始時間
start_time = time.time()

url = "https://www.ptt.cc/bbs/Stock/index.html"

root_url = "https://www.ptt.cc/"

platform = "PTT"

headers = {
  "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}

response = requests.get(url, headers = headers).text

# print(response)

soup = BeautifulSoup(response, "lxml")

# print(soup)

# 取得頁數
page = soup.select_one("div.btn-group.btn-group-paging a:nth-of-type(2)").get("href")

pattern= r"index(\d{4})"

page = int(re.search(pattern, page).group(1)) + 1


for i in range(10) :
  url = f"https://www.ptt.cc/bbs/Stock/index{ page }.html"

  response = requests.get(url, headers = headers).text

  soup = BeautifulSoup(response, "lxml")

  print(f"這是第 { page } 頁")


  datas = soup.select("div.r-ent")

  page -= 1

  for data in datas :
    if not data.find("span", class_ = ["hl f2", "hl f3"]) or\
      not data.find("a") :
      continue

    # 取得標題
    title = data.find("a").text

    # 取得作者
    author = data.find(class_ = "author").text
    
    # 取得內文連結
    link = data.find("a").get("href")
    link = urljoin(root_url, link)

    # 取得推文數
    push_count = int(data.find("span", class_ = ["hl f2", "hl f3"]).text)

    # 取得時間
    date = data.find(class_ = "date").text.strip()

    # 轉換成 datetime 物件
    date = datetime.strptime(date, "%m/%d").replace(year=2025)

    # 轉換為 str 格式 
    date = date.strftime("%Y-%m-%d")   


    # 查詢 SQL 語法
    sql = """
      SELECT platform, title, author, link, push_count, created_at FROM stock_news
      WHERE platform = %s AND title = %s
    """

    # 執行 SQL 語法
    cursor.execute(sql, (platform, title))

    result = cursor.fetchall()

    if not result :
      # 建立 SQL 語法
      sql = "INSERT INTO stock_news (platform, title, author, link, push_count, created_at) VALUES (%s, %s, %s, %s, %s, %s)"

      # 執行 SQL 語法
      cursor.execute(sql, (platform, title, author, link, push_count, date))

      # 立即提交
      conn.commit()

      print(title)
      print(author)
      print(date)
      print(link)
      print(push_count)
      print("-" * 50)      

    else :
      print(f"文章 {title} 已存在!!!")


# 記錄結束時間
end_time = time.time()

# 計算執行時間
execution_time = end_time - start_time
print(f"程式執行時間: {execution_time :.2f} 秒")

  