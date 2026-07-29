import pymysql

db = pymysql.connect(host="localhost", user="root", password="654321", database="mydb")

cursor = db.cursor()

try:
    cursor.execute("select * from user_table")
    # results = cursor.fetchall()
    # results = cursor.fetchone()
    results = cursor.fetchmany()
    print("###", results)
except pymysql.MySQLError:
    db.rollback()
    raise

db.close()
