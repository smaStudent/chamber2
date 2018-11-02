# from errors import ErrorDict        # to bedzie potrzebne do obslugi bledow
from functions import *
import serial
import dataStruct


class Chamber:
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600):
        self.timeInIteration = None
        self.iteration = 0

        self.ser = serial.Serial()

        self.ser.port = port
        self.ser.baudrate = baudrate
        self.ser.polarity = None
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.timeout = 1
        self.ser.write_timeout = 2
        self.ser.parity = serial.PARITY_NONE
        self.ser.dsrdtr = True
        self.periodOfRead = 20  # seconds
        self.amountOfDataInTabs = 100
        self.counter = 0
        self.tempFile = 'tempData.txt'
        self.humiFile = 'humiData.txt'

        # commands for having a response
        self.resetCommand = 'SRQ?\r\n'
        self.tempAsk = 'TEMP?\r\n'
        self.humiAsk = 'HUMI?\r\n'
        self.heaterAsk = '%?\r\n'
        self.condInside = 'MON?\r\n'
        # self.lastString = '\r\n'    # it has to be in every single message
        self.tempDataObject = dataStruct.dataStruct()
        self.humiDataObject = dataStruct.dataStruct()


        try:
            self.ser.open()
            print("We are connected with chamber")
        except serial.SerialException:
            # switch red Led for instance
            print("We couldnt connect with chamber, try again after checking it!")
            return serial.SerialException

    def __del__(self):
        self.ser.close()
        # saveToFile(self.tempFile, self.tempTab)
        # saveToFile(self.humiFile, self.humiTab)
        # here we can add feature like switch on red LED
        print("We end work for now, you have your data in files")

    def update(self):
        period = datetime.datetime.now()
        if period.second % self.periodOfRead == 0:
            try:
                self.tempData()
                self.humiData()
                return True
            except:
                return serial.SerialException
        else:
            return False

    ####################################
    ######### helpful function #########
    ####################################

    def tempData(self):
        # to jest do zmiany, bo nie dziala poprawnie
        try:
            PV, SP, lowVal, maxVal = changeAnsForTable(sendAndReceive(self.ser, self.tempAsk))
            self.tempDataObject.dateTime = self.timeInIteration
            self.tempDataObject.PV = PV
            self.tempDataObject.SP = SP
            self.tempDataObject.minLv = lowVal
            self.tempDataObject.maxLv = maxVal
            print("TEMP: ", self.tempDataObject)
            return self.tempDataObject
        except serial.SerialException:
            print("Lost connection with chamber")
            return serial.SerialException

    def humiData(self):
        # to jest do zmiany, bo nie dziala poprawnie
        try:
            PV, SP, lowVal, maxVal = changeAnsForTable(sendAndReceive(self.ser, self.humiAsk))
            self.humiDataObject.dateTime = self.timeInIteration
            self.humiDataObject.PV = PV
            self.humiDataObject.SP = SP
            self.humiDataObject.minLv = lowVal
            self.humiDataObject.maxLv = maxVal
            print("TEMP: ", self.humiDataObject)
            return self.humiDataObject
        except serial.SerialException:
            print("Lost connection with chamber")
            return serial.SerialException

    def getHumi(self):
        return self.humiDataObject

    def getTemp(self):
        return self.tempDataObject

#############################################################################
###########################   OLD CODE  #####################################
#############################################################################


# def showDate(self):
#     print(self.timeInIteration)
#
# def showTemp(self):
#     if self.ser.isOpen():
#         print(sendAndReceive(self.ser, self.tempAsk))
#         return sendAndReceive(self.ser, self.tempAsk)
#     else:
#         print("Lost connection with chamber")
#
# def showHumi(self):
#     if self.ser.isOpen():
#         print(sendAndReceive(self.ser, self.humiAsk))
#         return sendAndReceive(self.ser, self.humiAsk)
#     else:
#         print("Lost connection with chamber")




# 1 
