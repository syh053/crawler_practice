from flask import Flask, redirect, url_for
from route.index import routes

# 創建 Flask 實例
app = Flask(__name__)

app.register_blueprint(routes)

@app.route("/")
def redirect_to_index() :
  return redirect(url_for("routes.index"))


if __name__ == "__main__" :
  app.run(debug=True)  # 啟動 Flask，並設置 debug 模式為 True
