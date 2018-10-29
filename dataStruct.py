class dataStruct:
    def __init__(self, dateTime=None, PV=None, SP=None, min=None, max=None):
        self.dateTime = dateTime
        self.PV = PV
        self.SP = SP
        self.minLv = min
        self.maxLv = max

    def __str__(self):
        return str(self.dateTime) + str(', ') + str(self.PV) + str(', ') + str(self.SP) + str(', ') + str(self.minLv) \
               + str(', ') + str(self.maxLv)

    def saveToFile(self, fileName):
        f = open(fileName, 'a')
        f.write(self.__str__())
        f.close()
