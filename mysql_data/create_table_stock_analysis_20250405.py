#%%
from create_database_20250331 import cursor

# 建立 table 語句
sql = """
  CREATE TABLE IF NOT EXISTS analysis_datas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  date DATETIME NOT NULL,
  open FLOAT NOT NULL,
  high FLOAT NOT NULL,
  low FLOAT NOT NULL,
  close FLOAT NOT NULL,
  volume FLOAT NOT NULL,
  sma5 FLOAT,
  sma10 FLOAT,
  sma20 FLOAT
  )
"""
cursor.execute(sql)
