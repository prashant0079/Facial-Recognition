# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 00:28:56 2018

@author: hmagg
"""

#Create
import sqlite3
conn = sqlite3.connect('notification.db') # Warning: This file is created in the current directory
conn.execute("CREATE TABLE notif (id INTEGER PRIMARY KEY, name char(100) NOT NULL, time timestamp NOT NULL, read BOOL NOT NULL, image char(1000) NOT NULL)")
conn.commit()
conn.close()

#################################################################################33
#Insert
import sqlite3
conn = sqlite3.connect('notification.db') # Warning: This file is created in the current directory
conn.execute("INSERT INTO notif (name,time,read,image) VALUES ('Prashant', '2012-12-25 23:59:59', 0, '/dataset/prashant/aligned3.jpg')")
conn.commit()
conn.close()

#################################################################################33
#Read
import sqlite3
conn = sqlite3.connect('notification.db') # Warning: This file is created in the current directory
c = conn.cursor()
c.execute("SELECT * FROM notif")
print(c.fetchall())
c.close()
conn.close()


#################################################################################33
from datetime import datetime, timedelta
import sqlite3
names = ["prashant", "pm!"]
conn = sqlite3.connect('notification.db')
for name in names:
    c = conn.cursor()
    d = timedelta(minutes = 5)
    print(d)
    c.execute("SELECT * FROM notif where name = ? AND time > ? ", (str(name), str(datetime.now()-d)))
    print(str(datetime.now()-d))
    result = c.fetchall()
    c.close()
    if len(result) < 1:
        conn.execute("INSERT INTO notif (name,time) VALUES (?, ?)", (name, datetime.now()))
        conn.commit()

conn.close()



            