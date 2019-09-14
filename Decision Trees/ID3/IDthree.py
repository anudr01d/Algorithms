import traceback
import math 

class IDthree(object):
    ftCount = 0
    insCount = 0
    partCount = 0
    outputFile = "output.txt"
    inpData = []
    clsCount = []
    clsNames = []
    clsData = []
    clsEntropy = []
    condEntropy = []
    infoGain = []
    spClsID = int()
    spFeatID = int()

    @classmethod
    def input(cls):
        dataset, input_file, output_file = input("Enter names of the files dataset input-partition output-partition : ").split()    
        
        #Output file
        outputFile = output_file

        #Parse Dataset
        cls.parseData(dataset)
        
        #Parse Partition
        cls.parsePartitions(input_file)

    @classmethod
    def calcEntropy(cls, noCount, yesCount):
        ans = 0
        totalCount = noCount + yesCount
        s1 = (noCount / totalCount)
        s2 = (yesCount / totalCount)
        if s1 == 0 and s2 == 0:
            ans = 0
        elif s1 == 0 and s2 != 0:
            ans = (-1) * (s2 * ((math.log(s2) / math.log(2))))
        elif s1 != 0 and s2 == 0:
            ans = (-1) * (s1 * ((math.log(s1) / math.log(2))))
        else:
            ans = (-s1 * (math.log(s1) / math.log(2)) - (s2 * (math.log(s2) / math.log(2))))
        if ans == -0.0:
            return 0
        else:
            return ans

    @classmethod
    def calcCondEntropy(cls, noCount0, yesCount0, noCount1, yesCount1, yesCount2, noCount2):
        count0 = noCount0 + yesCount0
        count1 = noCount1 + yesCount1
        count2 = noCount2 + yesCount2
        totalCount = count0 + count1 + count2
        if count0 == 0 and count1 == 0 and count2 == 0:
            return 0
        if count0 == 0 and count1 == 0 and count2 != 0:
            return (count2 / totalCount) * cls.calcEntropy(noCount2, yesCount2)
        if count0 == 0 and count1 != 0 and count2 == 0:
            return (count1 / totalCount) * cls.calcEntropy(noCount1, yesCount1)
        if count0 == 0 and count1 != 0 and count2 != 0:
            return (count2 / totalCount) * cls.calcEntropy(noCount2, yesCount2) + (count1 / totalCount) * cls.calcEntropy(noCount1, yesCount1)
        if count0 != 0 and count1 == 0 and count2 == 0:
            return (count0 / totalCount) * cls.calcEntropy(noCount0, yesCount0)
        if count0 != 0 and count1 == 0 and count2 != 0:
            return (count0 / totalCount) * cls.calcEntropy(noCount0, yesCount0) + (count2 / totalCount) * cls.calcEntropy(noCount2, yesCount2)
        if count0 != 0 and count1 != 0 and count2 == 0:
            return (count0 / totalCount) * cls.calcEntropy(noCount0, yesCount0) + (count1 / totalCount) * cls.calcEntropy(noCount1, yesCount1)
        if count0 != 0 and count1 != 0 and count2 != 0:
            return (count0 / totalCount) * cls.calcEntropy(noCount0, yesCount0) + (count1 / totalCount) * cls.calcEntropy(noCount1, yesCount1) + (count2 / totalCount) * cls.calcEntropy(noCount2, yesCount2)
        return 0

    @classmethod
    def findMaxGain(cls):
        maxF = 0
        i = 0
        while i < cls.partCount:
            f = 0
            maxValue = 0
            maxFeatureID = 0
            j = 0
            while j < cls.ftCount - 1:
                if cls.infoGain[i][j] > maxValue:
                    maxValue = cls.infoGain[i][j]
                    maxFeatureID = j
                j += 1
            f = maxValue * (float(cls.clsCount[i]) / cls.insCount)
            if f > maxF:
                maxF = f
                cls.spClsID = i
                cls.spFeatID = maxFeatureID
            i += 1

    @classmethod
    def main(cls, args):
        try:
            cls.input()
            print("Input successful")

            cls.clsEntropy = [None] * cls.partCount
            i = 0
            while i < cls.partCount:
                yesCount = 0
                noCount = 0
                tCount = 0
                j = 0
                while j < cls.insCount:
                    k = 0
                    while k < cls.clsCount[i]:
                        if cls.clsData[i][k] == (j + 1) and cls.inpData[j][cls.ftCount - 1] == 1:
                            yesCount += 1
                        if cls.clsData[i][k] == (j + 1) and cls.inpData[j][cls.ftCount - 1] == 0:
                            noCount += 1
                        k += 1
                    j += 1
                cls.clsEntropy[i] = cls.calcEntropy(noCount, yesCount)
                i += 1

            cls.condEntropy = [ [ None for i in range(cls.ftCount - 1) ] for j in range(cls.partCount) ]
            cls.infoGain = [ [ None for i in range(cls.ftCount - 1) ] for j in range(cls.partCount) ]
            i = 0
            while i < cls.partCount:
                j = 0
                while j < cls.ftCount - 1:
                    yesCount0 = 0
                    noCount0 = 0
                    yesCount1 = 0
                    noCount1 = 0
                    noCount2 = 0
                    yesCount2 = 0
                    k = 0
                    while k < cls.clsCount[i]:
                        if cls.inpData[cls.clsData[i][k] - 1][j] == 0 and cls.inpData[cls.clsData[i][k] - 1][cls.ftCount - 1] == 0:
                            noCount0 += 1
                        elif cls.inpData[cls.clsData[i][k] - 1][j] == 0 and cls.inpData[cls.clsData[i][k] - 1][cls.ftCount - 1] == 1:
                            yesCount0 += 1
                        elif cls.inpData[cls.clsData[i][k] - 1][j] == 1 and cls.inpData[cls.clsData[i][k] - 1][cls.ftCount - 1] == 0:
                            noCount1 += 1
                        elif cls.inpData[cls.clsData[i][k] - 1][j] == 1 and cls.inpData[cls.clsData[i][k] - 1][cls.ftCount - 1] == 1:
                            yesCount1 += 1
                        elif cls.inpData[cls.clsData[i][k] - 1][j] == 2 and cls.inpData[cls.clsData[i][k] - 1][cls.ftCount - 1] == 0:
                            noCount2 += 1
                        elif cls.inpData[cls.clsData[i][k] - 1][j] == 2 and cls.inpData[cls.clsData[i][k] - 1][cls.ftCount - 1] == 1:
                            yesCount2 += 1
                        k += 1
                    cls.condEntropy[i][j] = cls.calcCondEntropy(noCount0, yesCount0, noCount1, yesCount1, noCount2, yesCount2)
                    cls.infoGain[i][j] = cls.clsEntropy[i] - cls.condEntropy[i][j]
                    j += 1
                i += 1
            print("Entropy calculation successful")

            cls.findMaxGain()
            print("Max gain successful")

            cls.writeOutput()
            print("output file created successfully")
        except Exception as e:
            traceback.print_exc()
            print("Partition unsuccessful...")

    @classmethod
    def parsePartitions(cls, fileName):
        line = None
        try:
            # Read the dataset file
            with open(fileName) as file_object:
                lines = file_object.readlines()
                for line in lines:
                    cls.partCount += 1

            cls.clsNames = [None] * cls.partCount
            cls.clsData = [ [ None for i in range(cls.insCount) ] for j in range(cls.partCount) ]
            cls.clsCount = [None] * cls.partCount
            j = 0
            
            for line in lines:
                line = line.rstrip()
                values = line.split(" ")
                cls.clsNames[j] = values[0]
                cls.clsCount[j] = 0
                i = 0
                while i < len(values)-1:
                    cls.clsCount[j] += 1
                    cls.clsData[j][i] = int(values[i + 1])
                    i += 1
                j += 1
            
        except Exception as ex:
            print("Partition file not found.")
            traceback.print_exc()

    @classmethod
    def parseData(cls, fileName):
        print(fileName)
        try:
            with open(fileName) as file_object:
                line = file_object.readline().rstrip()
                countString = line.split(" ")
                cls.insCount = int(countString[0])
                cls.ftCount = int(countString[1])
                cls.inpData = [ [ None for i in range(cls.ftCount) ] for j in range(cls.insCount) ]
                rowCount = 0

            with open(fileName) as fp:
                line = fp.readline().rstrip()
                line = fp.readline().rstrip()
                while line:
                    features = line.split(" ")
                    i = 0
                    while i<len(features):
                        cls.inpData[rowCount][i] = int(features[i])
                        i += 1
                    rowCount += 1
                    line = fp.readline().rstrip()

        except Exception as ex:
            print("Dataset file not found.")
            traceback.print_exc()

    @classmethod
    def writeOutput(cls):
        try:
            output = open(cls.outputFile, "w") 
            line = ""
            i = 0
            while i < cls.partCount:
                if i == cls.spClsID:
                    split1 = cls.clsNames[i] + "0"
                    split2 = cls.clsNames[i] + "1"
                    split3 = cls.clsNames[i] + "2"
                    j = 0
                    while j < cls.clsCount[i]:
                        if cls.inpData[cls.clsData[i][j] - 1][cls.spFeatID] == 1:
                            split1 = str(split1) + " " + str(cls.clsData[i][j])
                        if cls.inpData[cls.clsData[i][j] - 1][cls.spFeatID] == 0:
                            split2 = str(split2) + " " + str(cls.clsData[i][j])
                        if cls.inpData[cls.clsData[i][j] - 1][cls.spFeatID] == 2:
                            split3 = str(split3) + " " + str(cls.clsData[i][j])
                        j += 1
                    output.write(str(split1))
                    output.write("\n")
                    output.write(str(split2))
                    output.write("\n")
                    output.write(str(split3))
                    if i < cls.partCount:
                        output.write("\n")
                    print("Partition "+ str(cls.clsNames[i]) + " was replaced with partitions " + str(cls.clsNames[i]) + "0" + "," + str(cls.clsNames[i]) + "1" + " using Feature " + str((cls.spFeatID + 1)))
                else:
                    line = cls.clsNames[i]
                    j = 0
                    while j < cls.clsCount[i]:
                        line = str(line) + " " + str(cls.clsData[i][j])
                        j += 1
                    output.write(str(line))
                    if i < cls.partCount:
                        output.write("\n")
                i += 1
            output.close() 
        except IOError as e:
            traceback.print_exc()


if __name__ == '__main__':
    import sys
    IDthree.main(sys.argv)