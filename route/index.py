from flask import Blueprint, render_template
from .stock_news import stock_news 
from .stock_analysis import analysis


# 建立 stock_news blueprint
routes = Blueprint("routes", __name__)

routes.register_blueprint(stock_news, url_prefix = "/stock")

routes.register_blueprint(analysis, url_prefix = "/stock")


@routes.route("/index", methods = ["GET"])
def index():
  return render_template("index.html")
