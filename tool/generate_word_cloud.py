import sys
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))

from mysql_data.create_database_20250331 import cursor, conn
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt


# 搜尋新聞資料庫中的所有標題
sql = "SELECT title FROM stock_news"

cursor.execute(sql)

titles = cursor.fetchall()

text = "".join([title[0] for title in titles])

words = "".join(jieba.cut(text)) # 進行中文分詞

wordcloud = WordCloud(
  font_path = 'msjh.ttc', # 指定字體路徑
  width = 800,
  height = 600,
  background_color = 'white'
  ).generate(words)

print(wordcloud)

plt.figure(figsize = (10, 6)) # 創建一個指定大小（10x6 英寸）的圖形

plt.imshow(wordcloud, interpolation = 'bilinear') # 將 wordcloud 物件以影像的方式顯示出來

plt.axis('off') # 移除邊框線

img_path = "static/img/wordcloud.png"

wordcloud.to_file(img_path)

plt.show()
