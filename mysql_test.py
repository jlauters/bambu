import pymysql.cursors
import pymysql


connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='pbdb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
  with connection.cursor() as cursor:
  
    sql = "SELECT * FROM refs"
    cursor.execute(sql)
    result = cursor.fetchone()
    print(result)

finally:
  connection.close()
