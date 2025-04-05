import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

sys.path.append(str(project_root))


from flask import Blueprint, render_template
from datetime import datetime
from .stock_news import stock_news 
from .stock_analysis import analysis


from mysql_data.create_database_20250331 import conn, cursor


# 建立 stock_news blueprint
routes = Blueprint("routes", __name__)

routes.register_blueprint(stock_news, url_prefix = "/stock")

routes.register_blueprint(analysis, url_prefix = "/stock")


@routes.route("/index", methods = ["GET"])
def index():
  """顯示大盤指數技術圖"""
  # 搜尋 SQL 語句
  sql = """
    SELECT * FROM analysis_datas WHERE name = 'TWSE'
  """

  # 執行 SQL 語句
  cursor.execute(sql)

  # 將取得的資料放進 datas 變數
  datas = cursor.fetchall()

  # 將資料轉換成字典後傳出去給 html 使用
  stock_datas = {
    "date" : [],
    "values" : [],
    "volume" : [],
    "sma5" : [],
    "sma10" : [],
    "sma20" : []
  }

  # 逐一迭代資料放進字典中
  for data in datas :
    values = [data[3], data[6], data[5], data[4]] # 順序 open close low high
    stock_datas["date"].append(datetime.strftime(data[2], '%Y/%m/%d'))
    stock_datas["values"].append(values)
    stock_datas["volume"].append(data[7])
    stock_datas["sma5"].append(data[8])
    stock_datas["sma10"].append(data[9])
    stock_datas["sma20"].append(data[10])

  print(stock_datas["date"])


  return render_template("index.html", datas = stock_datas)


# 404 錯誤處理：導回首頁
@routes.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404  # 返回 404.html 並設定狀態碼r('routes.index'))
