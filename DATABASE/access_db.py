import pymysql

host = "10.200.37.130"   # ip address of server
user = "user"
password = "1234"
db = "capstone"

con = pymysql.connect(host, user, password, db, port=3307)
curs = con.cursor()


sql = "show tables;"

curs.execute(sql)
row = curs.fetchall()
print(row)
