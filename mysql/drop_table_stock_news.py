#%%
""" 刪除 stock_news 資料表 """
from create_database_20250331 import cursor

sql = "DROP TABLE IF EXISTS stock_news"

cursor.execute(sql)
