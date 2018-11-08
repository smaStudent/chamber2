from chamberClass import Chamber
from dataStruct import dataStruct
import time
from functions import *
import time
# import pymysql as mysql
import MySQLdb as mysql
import serial


def main():
    # variables
    tryCount = 0
    amountOfData = 0
    tempData = []
    humiData = []
    areWeWorking = False
    ##### Try to connect with chamber
    chamber = Chamber()
    areWeWorking = True
    print("Wykonane: chamber = Chamber()")



    while tryCount < 100 and not areWeWorking:
        try:
            print("1.1")
            chamber = Chamber()
            print("1.2")
            areWeWorking = True
            tryCount = 0
        except:
            print("Try again later, this was: " + str(tryCount) +
                  " try. CHECK CABLES AND WE WILL TRY AGAIN IN 10 seconds")
            areWeWorking = False
            print("areWeWorking", areWeWorking)
            tryCount += 1
            print("tryCount", tryCount)
            time.sleep(10)
    #### end of module which want to connect with chamber

    ######## module which is responsible for collectind data, and store that in the MySQL

    while areWeWorking:

        if chamber.update():
            tempttData = dataStruct(chamber.getTemp())
            humitData = dataStruct(chamber.getHumi())
            amountOfData += 1
            tempData.append(tempttData)
            humiData.append(humitData)
            print("udalo sie, po raz: ", amountOfData)




        if amountOfData == 5:
            print("weszlismy do if amountOfData == 5:")

            for i in tempData:

                saveSomeDataToMySQLTemp('mysql01.saxon.beep.pl',
                                        'sub_saxon',
                                        'passwd',
                                        'test_database',
                                        i)  # 'chamberTemp',

                i.saveToFile("tempData.txt")

            # for i in humiData:
            #
            #     saveSomeDataToMySQLHumi('mysql01.saxon.beep.pl',
            #                             'sub_saxon',
            #                             'passwd',
            #                             'test_database',
            #                             i)  # 'chamberHumi',
            #     i.saveToFile("humiData.txt")

            tempData = []
            humiData = []
            amountOfData = 0
                # if we would like to, we can add data also to the file and have local history



if __name__ == '__main__':
    main()
