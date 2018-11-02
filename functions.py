import time
import serial
import datetime
import MySQLdb as mysql
#import pymysql as mysql


def sendAndReceive(serialObject, message):
    if serialObject.isOpen():
        serialObject.write(bytearray(message, 'utf-8'))
        # time.sleep(0.2) we use flush() instead of time.sleep()
        serialObject.flush()
        ans = serialObject.readline()
        ans = ans.decode("utf-8")
        return ans


def retFloatFromString(givStr):
    retFloat = 0.0
    newFirstStr = str()
    newLastStr = str()
    wasThereComma = False

    for c in givStr:
        if c != '.' and not wasThereComma:
            newFirstStr = newFirstStr + c
        elif c != '.' and wasThereComma:
            newLastStr = newLastStr + c
        elif c == '.':
            wasThereComma = True

    if wasThereComma:
        retFloat = float(int(newFirstStr)) + (float(int(newLastStr)) / pow(10, (len(newLastStr))))
    else:
        retFloat = float(int(newFirstStr))
    return retFloat


def changeAnsForTable(ans):
    PV = 0.0
    SP = 0.0
    low = 0.0
    max = 0.0
    tempStr = str()
    iteration = 0

    for c in ans:
        if c != ',':
            tempStr = tempStr + c
        elif c == ',':
            if iteration == 0:
                PV = retFloatFromString(tempStr)
                tempStr = str()
            elif iteration == 1:
                if tempStr != "OFF":
                    SP = retFloatFromString(tempStr)
                tempStr = str()
            elif iteration == 2:
                max = retFloatFromString(tempStr)
                tempStr = str()
            elif iteration == 3:
                low = retFloatFromString(tempStr)
                tempStr = str()
            iteration = iteration + 1

    return PV, SP, low, max


def saveToFile(name, tab):
    file = open(name, "a")
    for i in tab:
        file.write(str(i)[1:-1] + "\n")

    file.close()


def saveObjectToFile(name, tab):
    file = open(name, 'a')
    for i in tab:
        file.write(i)
    print("udaloSieFILE", end=" ")
    file.close()


def saveSomeDataToMySQL(hostGiven, userGiven, passwdGiven, dbGiven, table, dataTab):
    try:
        connection = mysql.connect(host=hostGiven,
                                   user=userGiven,
                                   passwd=passwdGiven,
                                   db=dbGiven)

        try:
            with connection.cursor() as cursor:
                print("INSERT INTO chamberTemp (dateTime, PV, SP, minLevel, maxLevel) VALUES (%s, %s, %s, %s, %s)")
                cursor.execute(
                    "INSERT INTO "+table+" (dateTime, PV, SP, minLevel, maxLevel) VALUES (%s, %s, %s, %s, %s)",
                    (dataTab.dateTime, dataTab.PV, dataTab.SP, dataTab.minLv, dataTab.maxLv))
            connection.commit()
            print("udaloSieSQL", end=" ")
        except:
            print("Unable to add data to the MySQl server, try again!")
            return mysql.DatabaseError

        connection.close()
    except:
        print("Unable to connect with MySQL! Try again later!")
        return mysql.DatabaseError
