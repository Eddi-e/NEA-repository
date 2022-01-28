import time
import sqlite3
from datetime import datetime
datestore = 9
while True:
    weekofday = (datetime.today().weekday())
    time.sleep(3)
    if weekofday != datestore:
        con = sqlite3.connect('databaseforwebapp.db')
        cursor = con.cursor()        
        row = cursor.execute("SELECT * FROM scheduling")
        datestore = int(weekofday)
        print(datestore)


    else:
        con = sqlite3.connect('databaseforwebapp.db')
        cursor = con.cursor()
        datestore1 = str(datestore)
        row = cursor.execute("SELECT * FROM scheduling WHERE day LIKE trim(?)",('%'+datestore1+'%',))
        day = row.fetchall()
        print(day)