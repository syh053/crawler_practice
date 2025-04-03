from flask import Blueprint
from .stock_news import stock_news 


# 建立 stock_news blueprint
routes = Blueprint("routes", __name__)

routes.register_blueprint(stock_news, url_prefix = "/stock")
