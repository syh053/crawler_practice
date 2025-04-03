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

sql  = "CREATE DATABASE IF NOT EXISTS test DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci"

# 建立資料庫
cursor.execute(sql)

# 重新建立連線，連上 test 資料庫
conn = mysql.connector.connect(
  host = "localhost",
  database = "test",
  user = "root",
  password = "1234567890"
)

# 建立游標
cursor = conn.cursor()
