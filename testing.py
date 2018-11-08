
# import dataStruct
# import functions
import datetime
# import time
# import pymysql as mysql
#
# var = 1
# var += 1
# print(var)
#
# dataTab = dataStruct.dataStruct(datetime.datetime.now(), 13.0, 0.0, 0.0, 100.0)
#
# functions.saveSomeDataToMySQL('mysql01.saxon.beep.pl',
#                               'sub_saxon',
#                               'passwd',
#                               'test_database',
#                               'chamberHumi',
#                               dataTab)



dateTime = datetime.datetime.now()
dated = datetime.datetime(dateTime.year, dateTime.month, dateTime.day, dateTime.hour, dateTime.minute, dateTime.second)


print(dated)
