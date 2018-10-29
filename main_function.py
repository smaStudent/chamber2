from chamberClass import Chamber
from dataStruct import dataStruct
import time
from functions import *
import serial


def main():
    # module to check if we are starting properly
    tryCount = 0
    amountOfData = 0
    areWeWorking = True
    while tryCount < 100:
        try:
            chamber = Chamber()
            areWeWorking = True
            tryCount = 0
        except:
            areWeWorking = False
            print("Try again, we couldnt connect with chamber")

        tempData = []
        humiData = []
        ##############################################

        # module to run repeadly over and over

        while areWeWorking:

            try:
                temptData = dataStruct(chamber.getTemp())
                humitData = dataStruct(chamber.getHumi())
                tempData.append(temptData)                  # collecting data and if we succeed, we adding this to our table
                humiData.append(humitData)                  # collecting data and if we succeed, we adding this to our table
            except:
                print("We have a problem")
                # switch on RED LED for exaple
                break

            if amountOfData == 100:                         # check if we already have 100 piece of data in each tables
                #here we have to add this to the MySQL
                try:
                    saveSomeDataToMySQL( 'chamberTemp', tempData)
                    saveSomeDataToMySQL(, humiData)
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
