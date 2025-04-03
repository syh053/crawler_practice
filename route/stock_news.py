from flask import Blueprint

# 建立 stock_news blueprint
stock_news = Blueprint("stock_news", __name__)

@stock_news.route("/news", methods = ["GET"])
def get_stock_news() :
  """ stock_news 路由 """
  return "TEST"