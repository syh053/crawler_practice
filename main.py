from flask import Flask
from route.index import routes

# 創建 Flask 實例
app = Flask(__name__)

app.register_blueprint(routes)


if __name__ == "__main__" :
  app.run(debug=True)  # 啟動 Flask，並設置 debug 模式為 True
