#%%
""" 刪除 analysis_datas 資料表 """
from create_database_20250331 import cursor

sql = "DROP TABLE IF EXISTS analysis_datas"

cursor.execute(sql)
