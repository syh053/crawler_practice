from flask import Blueprint, render_template, request
from mysql_data.create_database_20250331 import conn, cursor
from flask_paginate import Pagination
from tool.count_datas import get_count


# 建立 stock_news blueprint
stock_news = Blueprint("stock_news", __name__)

@stock_news.route("/news", methods = ["GET"])
def get_stock_news() :
  """ stock_news 新聞路由 """

  # 設定 limit
  limit = 10

  # 取得分頁
  page = request.args.get("page", type = int, default = 1)

  # 取得平台
  platform = request.args.get("platform", "")

  # 取得作者
  author = request.args.get("author", "")

  # 取得推文樹
  push_count = request.args.get("push_count", "")

  # 將所有參數整合到字典中
  search_params = {
      'page': page,
      'platform': platform,
      'author': author,
      'push_count': push_count
  }


  if page == 1 and platform == "" and author == "" and push_count == "": 
    print(111)
    # 取得資料數量
    count = get_count("")

    # 搜尋全部資料
    sql = "SELECT * FROM stock_news LIMIT %s, %s" 

    start_page = page - 1

    params = (start_page * limit, limit)

    # 執行 SQL 指令
    cursor.execute(sql, params)

    # 將搜尋到的資料存進 datas 變數
    datas = cursor.fetchall()


  elif platform == "" and author == "" and push_count == "" : 
    print(222)
    # 取得資料數量
    count = get_count("")

    # 搜尋全部資料
    sql = "SELECT * FROM stock_news LIMIT %s, %s" 

    start_page = page - 1

    params = (start_page * limit, limit)

    # 執行 SQL 指令
    cursor.execute(sql, params)

    # 將搜尋到的資料存進 datas 變數
    datas = cursor.fetchall()


  elif platform != "" and author == "" and push_count == "" : 
    print(333)
    # 取得資料數量
    count = get_count("WHERE platform LIKE '%{}%'".format(platform))

    # 搜尋全部資料
    sql = "SELECT * FROM stock_news WHERE platform LIKE %s LIMIT %s, %s" 

    start_page = page - 1

    params = (f"%{platform}%", start_page * limit, limit)

    # 執行 SQL 指令
    cursor.execute(sql, params)

    # 將搜尋到的資料存進 datas 變數
    datas = cursor.fetchall()


  elif platform == "" and author != "" and push_count == "": 
    print(444)
    # 取得資料數量
    count = get_count("WHERE author LIKE '%{}%'".format(author))

    # 搜尋全部資料
    sql = "SELECT * FROM stock_news WHERE author LIKE %s LIMIT %s, %s" 

    start_page = page - 1

    params = (f"%{author}%", start_page * limit, limit)

    # 執行 SQL 指令
    cursor.execute(sql, params)

    # 將搜尋到的資料存進 datas 變數
    datas = cursor.fetchall()


  elif platform == "" and author == "" and push_count != "": 
    print(555)
    # 取得資料數量
    count = get_count("WHERE push_count >= {}".format(push_count))

    # 搜尋全部資料
    sql = "SELECT * FROM stock_news WHERE push_count >= %s LIMIT %s, %s" 

    start_page = page - 1

    params = (push_count, start_page * limit, limit)

    # 執行 SQL 指令
    cursor.execute(sql, params)

    # 將搜尋到的資料存進 datas 變數
    datas = cursor.fetchall()


  elif platform != "" and author != "" and push_count == "" : 
    print(666)
    # 取得資料數量
    count = get_count("WHERE platform LIKE '%{}%' AND author LIKE '%{}%'".format(platform, author))

    # 搜尋全部資料
    sql = "SELECT * FROM stock_news WHERE platform LIKE %s AND author LIKE %s LIMIT %s, %s" 

    start_page = page - 1

    params = (f"%{platform}%", f"%{author}%", start_page * limit, limit)

    # 執行 SQL 指令
    cursor.execute(sql, params)

    # 將搜尋到的資料存進 datas 變數
    datas = cursor.fetchall()


  elif platform == "" and author != "" and push_count!= "" : 
    print(777)
    # 取得資料數量
    count = get_count("WHERE author LIKE '%{}%' AND push_count >= {}".format(author, push_count))

    # 搜尋全部資料
    sql = "SELECT * FROM stock_news WHERE author LIKE %s AND push_count >= %s LIMIT %s, %s" 

    start_page = page - 1

    params = (f"%{author}%", push_count, start_page * limit, limit)

    # 執行 SQL 指令
    cursor.execute(sql, params)

    # 將搜尋到的資料存進 datas 變數
    datas = cursor.fetchall()


  elif platform != "" and author == "" and push_count!= "" : 
    print(888)
    # 取得資料數量
    count = get_count("WHERE platform LIKE '%{}%' AND push_count >= {}".format(platform, push_count))

    # 搜尋全部資料
    sql = "SELECT * FROM stock_news WHERE platform LIKE %s AND push_count >= %s LIMIT %s, %s" 

    start_page = page - 1

    params = (f"%{platform}%", push_count, start_page * limit, limit)

    # 執行 SQL 指令
    cursor.execute(sql, params)

    # 將搜尋到的資料存進 datas 變數
    datas = cursor.fetchall()


  else : 
    print(999)
    # 取得資料數量
    count = get_count("WHERE platform LIKE '%{}%' AND author LIKE '%{}%' AND push_count >= {}".format(platform, author, push_count))

    # 搜尋全部資料
    sql = "SELECT * FROM stock_news WHERE platform LIKE %s AND author LIKE %s AND push_count >= %s LIMIT %s, %s" 

    start_page = page - 1

    params = (f"%{platform}%", f"%{author}%", push_count, start_page * limit, limit)

    # 執行 SQL 指令
    cursor.execute(sql, params)

    # 將搜尋到的資料存進 datas 變數
    datas = cursor.fetchall()



  # 使用 Flask-Paginate 來實現分頁功能，用來控制當前頁面、總資料數量、每頁顯示筆數
  pagination = Pagination(
    page = page, # 當前頁碼
    total = count, # 總資料筆數
    per_page = limit # 每頁顯示 15 筆
  )

  return render_template("news.html", datas = datas, params = search_params, pagination = pagination)
