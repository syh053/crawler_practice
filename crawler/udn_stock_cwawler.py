#%%
from pathlib import Path
import sys

# 設定 project_root
project_root = Path(__file__).resolve().parent.parent

sys.path.append(str(project_root))


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import requests
from bs4 import BeautifulSoup


from mysql_data.create_database_20250331 import conn, cursor


# 啟用 Chrome 驅動器
driver = webdriver.Chrome()

# 網址
url = "https://udn.com/news/cate/2/6645"

headers = {
  "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}

platform = "UDN"

# 開啟 url 
driver.get(url)

# 找到父元素
parent = driver.find_elements(By.CSS_SELECTOR, ".thumb-news.more-news.thumb-news--big.context-box")[1]

# 重複點擊 More 按鈕 3 次
for i in range(3) :
  try :
    # 等待 More 元素可點擊
    button = WebDriverWait(parent, 5).until(
      EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-ripple.btn-more.btn-more--news"))
    )

    # 滾動到元素所在位置
    ActionChains(driver).move_to_element(button).perform()

    # 點擊 More 按鈕
    button.click()

  except :
    continue

# 定位資料 table 
table = parent.find_element(By.CSS_SELECTOR, ".context-box__content.story-list__holder.story-list__holder--full")

# 定位 dataas
datas = table.find_elements(By.CLASS_NAME, "story-list__news")



for data in datas :
  # 取得 a 標籤內容
  a_tag = data.find_element(By.TAG_NAME, "a")

  # 取得標籤
  title = a_tag.get_attribute("title")
  
  # 相片連結
  img = data.find_element(By.TAG_NAME, "img").get_attribute("src")

  # 取得時間
  date = data.find_element(By.TAG_NAME, "time").text
  # 轉換成 datetime 物件
  date = datetime.strptime(date, "%Y-%m-%d %H:%M").replace(second=0)
  # 轉換為 str 格式
  date = date.strftime("%Y-%m-%d %H:%M:%S")

  # 內文連結
  link = a_tag.get_attribute("href")


  """ 使用 requests 發出 GET 請求取得內文資料 """ 
  response = requests.get(link, headers = headers).text

  soup = BeautifulSoup(response, "lxml")

  # 取得作者
  author = soup.select_one("section.authors a")

  # 確認是否有作者，沒有的話就找報社
  if author :
    author = author.text
    
  else :
    # 連報社都沒有就跳過
    if soup.select_one("section.authors .article-content__author"):
      author = soup.select_one("section.authors .article-content__author")
      author = author.text.strip().split("／")[0]

    else:
      continue

  # 取得內文
  words = soup.select("div.article-content__paragraph p")

  content = ""
  

  for word in words :
    content += word.text


  # 查詢 SQL 語法
  sql = """
    SELECT platform, title, author, link, push_count, created_at FROM stock_news
    WHERE platform = %s AND title = %s
  """

  # 執行 SQL 語法
  cursor.execute(sql, (platform, title))

  result = cursor.fetchall()

  if not result :
    sql = """
    INSERT INTO stock_news (platform, title, author, link, img, content, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(sql, (platform, title, author, link, img, content, date))
      
    # 立即提交
    conn.commit()  

    print(title)
    print(author)
    print(link)
    print(img)
    print(date)
    print(content)
    print()

  else :
    print(f"文章 {title} 已存在!!!")


# 關閉 driver
driver.close()
