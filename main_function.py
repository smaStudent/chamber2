from chamberClass import Chamber
from dataStruct import dataStruct
import time
from functions import *
import serial


def main():
    # variables
    tryCount = 0
    amountOfData = 0
    tempData = []
    humiData = []
    ##### Try to connect with chamber
    try:
        chamber = Chamber()
        areWeWorking = True
    except:
        while tryCount < 100:
            try:
                chamber = Chamber()
                areWeWorking = True
                tryCount = 0
            except:
                print("Try again later, this was: " + str(tryCount) +
                      "try. CHECK CABLES AND WE WILL TRY AGAIN IN 10 seconds")
                areWeWorking = False
                tryCount += tryCount
    #### end of module which want to connect with chamber

    ######## module which is responsible for collectind data, and store that in the MySQL

    while areWeWorking:
        try:
            if chamber.update():
                temptData = dataStruct(chamber.getTemp())
                humitData = dataStruct(chamber.getHumi())
                amountOfData += 1

            if amountOfData == 100:
                for i in tempData:
                    saveSomeDataToMySQL('mysql01.saxon.beep.pl',
                                        'sub_saxon',
                                        'passwd',
                                        'test_database',
                                        'chamberTemp',
                                        i)

                for i in humiData:
                    saveSomeDataToMySQL('mysql01.saxon.beep.pl',
                                        'sub_saxon',
                                        'passwd',
                                        'test_database',
                                        'chamberHumi',
                                        i)

                tempData = []
                humiData = []
                amountOfData = 0
        except:
            print("Unable to update chamber!")

        ##############################################

        while areWeWorking:

            try:
                if chamber.update():
                    tempData.append(temptData)  # collecting data and if we succeed, we adding this to our table
                    humiData.append(humitData)  # collecting data and if we succeed, we adding this to our table
                    print(tempData)
                    print(humiData)
            except:
                print("We have a problem, we couldn't update the chamber")
                # switch on RED LED for exaple
                break

            if amountOfData == 100:  # check if we already have 100 piece of data in each tables
                # here we have to add this to the MySQL
                try:
                    saveSomeDataToMySQL('mysql01.saxon.beep.pl', 'sub_saxon', 'passwd', 'test_database', 'chamberTemp',
                                        tempData)
                    saveSomeDataToMySQL('mysql01.saxon.beep.pl', 'sub_saxon', 'passwd', 'test_database', 'chamberHumi',
                                        humiData)
                    saveObjectToFile("tempData.txt", tempData)
                    saveObjectToFile("HumiData.txt", humiData)
                    print("Adding corectly to MySQl database")
                except mysql.err.Error:
                    saveObjectToFile("tempData.txt", tempData)
                    saveObjectToFile("HumiData.txt", humiData)
                    print("Added data just to the files")
                amountOfData = 0
                tempData.clear()
                humiData.clear()
            else:
                amountOfData += 1

        # if we are here, we will give 15 second for user to solve the connection problem etc.
        time.sleep(15)
        # adding one to tryCount
        tryCount += 1
        ##############################################


if __name__ == '__main__':
    main()
