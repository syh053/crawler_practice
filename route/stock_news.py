from flask import Blueprint, render_template
from mysql_data.create_database_20250331 import conn, cursor


# 建立 stock_news blueprint
stock_news = Blueprint("stock_news", __name__)

@stock_news.route("/news", methods = ["GET"])
def get_stock_news() :
  """ stock_news 新聞路由 """

  # 計算 news 表中所有記錄的總數，並將結果命名為 nc
  sql = "SELECT COUNT(*) AS nc FROM stock_news"

  # 執行 SQL 指令
  cursor.execute(sql)

  # 將返回 tuple 格式
  datacount = cursor.fetchone()

  count = datacount[0]

  # 搜尋全部資料
  sql = "SELECT * FROM stock_news" 

  # 執行 SQL 指令
  cursor.execute(sql)

  # 將搜尋到的資料存進 datas 變數
  datas = cursor.fetchall()

  return render_template("stock.html", datas = datas)
