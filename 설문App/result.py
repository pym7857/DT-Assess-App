import pandas as pd
import pymysql

db = pymysql.connect(
        host='127.0.0.1', 
        port=3306, 
        user='root', 
        passwd='1562', 
        db='test1', 
        charset='utf8'
    )
cursor = db.cursor(pymysql.cursors.DictCursor)
sql = "SELECT * FROM `test1_table`;"
cursor.execute(sql)
result = cursor.fetchall()

result = pd.DataFrame(result)
print(result)