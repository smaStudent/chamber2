import dataStruct
import functions
import datetime
import time

var = 1
var += 1
print(var)

data1 = dataStruct.dataStruct(datetime.datetime.now(), 13.0, 0.0, 0.0, 100.0)
time.sleep(1)
data2 = dataStruct.dataStruct(datetime.datetime.now(), 16.0, 0.1, 0.0, 1010.0)

functions.saveSomeDataToMySQL('mysql01.saxon.beep.pl',
                              'sub_saxon',
                              'passwd',
                              'test_database',
                              'chamberTemp',
                              data1)
