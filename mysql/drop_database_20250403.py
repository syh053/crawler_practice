#%%
"""刪除 test 資料庫"""
import mysql.connector

# 建立連線
conn = mysql.connector.connect(
  host = "localhost",
  user = "root",
  password = "1234567890"
)

sql = "DROP DATABASE IF EXISTS test"

# 建立游標
cursor = conn.cursor()

cursor.execute(sql)
