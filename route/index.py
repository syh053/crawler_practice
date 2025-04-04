from flask import Blueprint, render_template, redirect, url_for
from .stock_news import stock_news 
from .stock_analysis import analysis


# 建立 stock_news blueprint
routes = Blueprint("routes", __name__)

routes.register_blueprint(stock_news, url_prefix = "/stock")

routes.register_blueprint(analysis, url_prefix = "/stock")


@routes.route("/index", methods = ["GET"])
def index():
  return render_template("index.html")


# 404 錯誤處理：導回首頁
@routes.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404  # 返回 404.html 並設定狀態碼r('routes.index'))
