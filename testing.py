import dataStruct
# import functions
import datetime

# import time
temp1 = datetime.datetime.now()

temp2 = datetime.datetime(temp1.year, temp1.month, temp1.day, temp1.hour, temp1.minute, temp1.second)

dataObj = dataStruct.dataStruct(te)

import pymysql as mysql

connection = mysql.connect('mysql01.saxon.beep.pl',
                           'sub_saxon',
                           'passwd',
                           'test_database')

with connection.cursor() as cursor:
    cursor.execute(
        "INSERT INTO chamberTemp (dateTime, PV, SP, minLevel, maxLevel) VALUES (%s, %s, %s, %s, %s)",
        (dataObj.dateTime, dataObj.PV, dataObj.SP, dataObj.minLv, dataObj.maxLv))
    print("1.2")
    connection.commit()
connection.close()
