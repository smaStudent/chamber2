import time
import serial
import datetime
import pymysql as mysql


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
        file.write(str(i)[1:-1]+"\n")

    file.close()

def saveObjectToFile(name, tab):
    file = open(name, 'a')
    for i in tab:
        file.write(i)

    file.close()

def saveSomeDataToMySQL(hostGiven, userGiven, passwdGiven, dbGiven, table, dataTab):
    connection = mysql.connect(host=hostGiven,
                               user=userGiven,
                               passwd=passwdGiven,
                               db=dbGiven)

    try:
        with connection.cursor() as cursor:
            # Create a new record
            for i in dataTab:
                cursor.execute("INSERT INTO "+table+" (dateTime, PV, SP, minLevel, maxLevel)"
                               "VALUES (%s, %f, %f, %f)",
                               (i.dateTime, i.PV, i.SP, i.minLv, i.maxLv))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
            connection.commit()
    except:
        print("Trouble with sending data to MySQL!!!")
        # here we can add sth like switching on red LED
        return mysql.err.Error
    finally:
        connection.close()