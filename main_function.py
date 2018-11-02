from chamberClass import Chamber
from dataStruct import dataStruct
import time
from functions import *
import time
import serial


def main():
    # variables
    tryCount = 0
    amountOfData = 0
    tempData = []
    humiData = []
    saveDataInIteration = False
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
                time.sleep(10)
    #### end of module which want to connect with chamber

    ######## module which is responsible for collectind data, and store that in the MySQL

    while areWeWorking:
        try:
            if chamber.update():
                tempData = dataStruct(chamber.getTemp())
                humiData = dataStruct(chamber.getHumi())
                amountOfData += 1

            if amountOfData == 5 and not saveDataInInteration:
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
                saveDataInIteration = True
                # if we would like to, we can add data also to the file and have local history

        except:
            print("Unable to update chamber or there is a problem with saving it in the MySQL!")





if __name__ == '__main__':
    main()
