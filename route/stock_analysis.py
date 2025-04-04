from flask import Blueprint, render_template

# 建立 analysis blueprint
analysis = Blueprint("analysis", __name__)

@analysis.route("/analysis", methods = ["GET"])
def analysis_show() :
  return render_template("analysis.html")