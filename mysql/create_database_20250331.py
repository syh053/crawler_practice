#%%
"""建立 test 資料庫"""

import mysql.connector

# 建立連線
conn = mysql.connector.connect(
  host = "localhost",
  user = "root",
  password = "1234567890"
)

# 建立游標
cursor = conn.cursor()

# 建立資料庫
cursor.execute("CREATE DATABASE IF NOT EXISTS test")

# 確認資料庫是否建立成功
cursor.execute("SHOW DATABASES")

# 擷取所有結果
databases = cursor.fetchall()

# 逐一迭代所有資料庫，確認有 test 資料庫
for db in databases:
  print(db[0])
