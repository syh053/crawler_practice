from flask import Blueprint, render_template, send_file

# 建立 word_cloud blueprint
wc = Blueprint("word_cloud", __name__)

@wc.route("/")
def newscloud() :
  return render_template("cloud.html")


@wc.route("/wordcloud")
def wordcloud() :
    return send_file("static/img/wordcloud.png", mimetype = "image/png")
