#%%
import sys

# 設定 project_root
project_root = r"C:\Users\ANDY\OneDrive\桌面\my_project"

# 加入 project_root 讓 Python 能找到 B 模組
sys.path.append(project_root)


import aiohttp
import asyncio
import nest_asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
from datetime import datetime
import time


from mysql_data.create_database_20250331 import conn, cursor

nest_asyncio.apply()

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}

root_url = "https://www.ptt.cc/"

platform = "PTT"


async def fetch(session, url) :
  async with session.get(url, headers = headers) as response :
    data = await response.text()

    return data

async def get_page(session, url) :
  """爬取最後一頁內容"""
  response = await fetch(session, url)

  soup = BeautifulSoup(response, "lxml")

  page_link = soup.select_one("div.btn-group.btn-group-paging a:nth-of-type(2)").get("href")

  pattern = r"index(\d{4})"

  page = int(re.search(pattern, page_link).group(1)) + 1

  return page


async def scrape_page(session, page):
  """爬取 PTT 股票版指定頁數的文章資訊"""
  url = f"https://www.ptt.cc/bbs/Stock/index{ page }.html"

  response = await fetch(session, url)

  soup = BeautifulSoup(response, "lxml")

  datas = soup.select("div.r-ent")
  
  return datas

async def parer_response(datas, page) :

  print(f"這是第 { page } 頁")
  
  for data in datas:
      if not data.find("span", class_ = ["hl f2", "hl f3"]) or\
        not data.find("a") :
        continue
      
      title = data.find("a").text
      author = data.find(class_ = "author").text # 取得作者
      link = urljoin(root_url, data.find("a").get("href"))
      push_count = int(data.find("span", class_=["hl f2", "hl f3"]).text)

      
      date = data.find(class_ = "date").text.strip() # 取得時間
      date = datetime.strptime(date, "%m/%d").replace(year=2025) # 轉換成 datetime 物件
      date = date.strftime("%Y-%m-%d") # 轉換為 str 格式 

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
        print(link)
        print(push_count)
        print("-" * 50)

      else :
        print(f"文章 {title} 已存在!!!")



async def main() :
  async with aiohttp.ClientSession() as session :
    url = "https://www.ptt.cc/bbs/Stock/index.html"

    page = await get_page(session, url)

    pages = [page - i for i in range(10) ]

    tasks = [ scrape_page(session, page) for page in pages ]

    results = await asyncio.gather(*tasks)

    for i, task in enumerate(results) :
      await parer_response(task, page - i)


if __name__ == "__main__" :
  # 記錄開始時間
  start_time = time.time()

  asyncio.run(main())

  # 記錄結束時間
  end_time = time.time()

  # 計算執行時間
  execution_time = end_time - start_time
  print(f"程式執行時間: {execution_time :.2f} 秒")
