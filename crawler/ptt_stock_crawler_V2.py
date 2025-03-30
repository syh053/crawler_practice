#%%
import aiohttp
import asyncio
import nest_asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import time

nest_asyncio.apply()

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}

root_url = "https://www.ptt.cc/"


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
      link = urljoin(root_url, data.find("a").get("href"))
      push_count = int(data.find("span", class_=["hl f2", "hl f3"]).text)
      print(title)
      print(link)
      print(push_count)
      print("-" * 50)


async def main() :
  async with aiohttp.ClientSession() as session :
    url = "https://www.ptt.cc/bbs/Stock/index.html"

    page = await get_page(session, url)

    pages = [page - i for i in range(100) ]

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
