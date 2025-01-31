import pickle
import mysql.connector as sql_con


con = sql_con.connect(host="localhost", user="root", password="AsteroidImpact000")
cur=con.cursor()
#sql="drop database bill;"
#cur.execute(sql)
SQL = "create database bill"


cur.execute(SQL)
SQL = "USE Bill"
cur.execute(SQL)
con.commit()

SQL = "CREATE TABLE BillInfo(SNo int(3), Name varchar(30), Qty int(3), Price int(4), TotalPrice int(4)); "
cur.execute(SQL)
con.commit()

f = open("details.txt","wb")
data = {'Apples': [50, 200, 'Sufficient stock'],
        'Banana': [50, 120, 'Sufficient stock'],
        'Broccoli': [50, 80, 'Sufficient stock'],
        'Cauliflower': [50, 60, 'Sufficient stock'],
        'Guava': [50, 50, 'Sufficient stock'],
        'Mango': [50, 350, 'Sufficient stock'],
        'Okra': [50, 60, 'Sufficient stock'],
        'Onion': [50, 40, 'Sufficient stock'],
        'Potato': [50, 25, 'Sufficient stock'],
        'Spinach': [50, 45, 'Sufficient stock'],
        'Tomato': [50, 60, 'Sufficient stock'],
        'Watermelon': [50, 30, 'Sufficient stock']}
##new = {}
##for k,v in data.items():
##    new[v[0]]= v[1:]
##data = new

pickle.dump(data,f)
f.close()

