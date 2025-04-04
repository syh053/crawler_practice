from mysql_data.create_database_20250331 import cursor


def get_count(condition) :
  # 計算 news 表中所有記錄的總數，並將結果命名為 nc
  sql = f"SELECT COUNT(*) AS nc FROM stock_news { condition }"

  # 執行 SQL 指令
  cursor.execute(sql)

  # 將返回 tuple 格式
  datacount = cursor.fetchone()

  return int(datacount[0])

