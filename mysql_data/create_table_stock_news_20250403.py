#%%
""" 建立 stock_news 資料表 """
from create_database_20250331 import cursor

sql = """
  CREATE TABLE IF NOT EXISTS stock_news (
    id INT AUTO_INCREMENT PRIMARY KEY,
    platform VARCHAR(255),
    title VARCHAR(255) NOT NULL,
    author VARCHAR(150),
    link VARCHAR(255),
    img VARCHAR(255),
    push_count INT NOT NULL,
    content TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP)
"""

cursor.execute(sql)
