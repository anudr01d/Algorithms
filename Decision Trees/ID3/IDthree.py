import traceback
import math 

class IDthree(object):
    featureCount = 0
    instanceCount = 0
    partitionCount = 0
    outputFile = "output.txt"
    inputData = []
    classCount = []
    classNames = []
    classData = []
    classEntropy = []
    conditionalEntropy = []
    informationGain = []
    splitClassID = int()
    splitFeatureID = int()

    @classmethod
    def input(cls):
        dataset, input_file, output_file = input("Enter names of the files dataset input-partition output-partition : ").split()    
        
        #Output file
        outputFile = output_file

        #Parse Dataset
        cls.parseDataset(dataset)
        
        #Parse Partition
        cls.parsePartitions(input_file)

    @classmethod
    def calculateEntropy(cls, noCount, yesCount):
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
    def calculateConditionalEntropy(cls, noCount0, yesCount0, noCount1, yesCount1, yesCount2, noCount2):
        count0 = noCount0 + yesCount0
        count1 = noCount1 + yesCount1
        count2 = noCount2 + yesCount2
        totalCount = count0 + count1 + count2
        if count0 == 0 and count1 == 0 and count2 == 0:
            return 0
        if count0 == 0 and count1 == 0 and count2 != 0:
            return (count2 / totalCount) * cls.calculateEntropy(noCount2, yesCount2)
        if count0 == 0 and count1 != 0 and count2 == 0:
            return (count1 / totalCount) * cls.calculateEntropy(noCount1, yesCount1)
        if count0 == 0 and count1 != 0 and count2 != 0:
            return (count2 / totalCount) * cls.calculateEntropy(noCount2, yesCount2) + (count1 / totalCount) * cls.calculateEntropy(noCount1, yesCount1)
        if count0 != 0 and count1 == 0 and count2 == 0:
            return (count0 / totalCount) * cls.calculateEntropy(noCount0, yesCount0)
        if count0 != 0 and count1 == 0 and count2 != 0:
            return (count0 / totalCount) * cls.calculateEntropy(noCount0, yesCount0) + (count2 / totalCount) * cls.calculateEntropy(noCount2, yesCount2)
        if count0 != 0 and count1 != 0 and count2 == 0:
            return (count0 / totalCount) * cls.calculateEntropy(noCount0, yesCount0) + (count1 / totalCount) * cls.calculateEntropy(noCount1, yesCount1)
        if count0 != 0 and count1 != 0 and count2 != 0:
            return (count0 / totalCount) * cls.calculateEntropy(noCount0, yesCount0) + (count1 / totalCount) * cls.calculateEntropy(noCount1, yesCount1) + (count2 / totalCount) * cls.calculateEntropy(noCount2, yesCount2)
        return 0

    @classmethod
    def findMaxGainFeature(cls):
        maxF = 0
        i = 0
        while i < cls.partitionCount:
            f = 0
            maxValue = 0
            maxFeatureID = 0
            j = 0
            while j < cls.featureCount - 1:
                if cls.informationGain[i][j] > maxValue:
                    maxValue = cls.informationGain[i][j]
                    maxFeatureID = j
                j += 1
            f = maxValue * (float(cls.classCount[i]) / cls.instanceCount)
            if f > maxF:
                maxF = f
                cls.splitClassID = i
                cls.splitFeatureID = maxFeatureID
            i += 1

    @classmethod
    def main(cls, args):
        """ main method """
        try:
            cls.input()
            print("Input successful")

            cls.classEntropy = [None] * cls.partitionCount
            i = 0
            while i < cls.partitionCount:
                yesCount = 0
                noCount = 0
                tCount = 0
                j = 0
                while j < cls.instanceCount:
                    k = 0
                    while k < cls.classCount[i]:
                        if cls.classData[i][k] == (j + 1) and cls.inputData[j][cls.featureCount - 1] == 1:
                            yesCount += 1
                        if cls.classData[i][k] == (j + 1) and cls.inputData[j][cls.featureCount - 1] == 0:
                            noCount += 1
                        k += 1
                    j += 1
                cls.classEntropy[i] = cls.calculateEntropy(noCount, yesCount)
                i += 1

            cls.conditionalEntropy = [ [ None for i in range(cls.featureCount - 1) ] for j in range(cls.partitionCount) ]
            cls.informationGain = [ [ None for i in range(cls.featureCount - 1) ] for j in range(cls.partitionCount) ]
            i = 0
            while i < cls.partitionCount:
                j = 0
                while j < cls.featureCount - 1:
                    yesCount0 = 0
                    noCount0 = 0
                    yesCount1 = 0
                    noCount1 = 0
                    noCount2 = 0
                    yesCount2 = 0
                    k = 0
                    while k < cls.classCount[i]:
                        if cls.inputData[cls.classData[i][k] - 1][j] == 0 and cls.inputData[cls.classData[i][k] - 1][cls.featureCount - 1] == 0:
                            noCount0 += 1
                        elif cls.inputData[cls.classData[i][k] - 1][j] == 0 and cls.inputData[cls.classData[i][k] - 1][cls.featureCount - 1] == 1:
                            yesCount0 += 1
                        elif cls.inputData[cls.classData[i][k] - 1][j] == 1 and cls.inputData[cls.classData[i][k] - 1][cls.featureCount - 1] == 0:
                            noCount1 += 1
                        elif cls.inputData[cls.classData[i][k] - 1][j] == 1 and cls.inputData[cls.classData[i][k] - 1][cls.featureCount - 1] == 1:
                            yesCount1 += 1
                        elif cls.inputData[cls.classData[i][k] - 1][j] == 2 and cls.inputData[cls.classData[i][k] - 1][cls.featureCount - 1] == 0:
                            noCount2 += 1
                        elif cls.inputData[cls.classData[i][k] - 1][j] == 2 and cls.inputData[cls.classData[i][k] - 1][cls.featureCount - 1] == 1:
                            yesCount2 += 1
                        k += 1
                    cls.conditionalEntropy[i][j] = cls.calculateConditionalEntropy(noCount0, yesCount0, noCount1, yesCount1, noCount2, yesCount2)
                    cls.informationGain[i][j] = cls.classEntropy[i] - cls.conditionalEntropy[i][j]
                    j += 1
                i += 1
            print("Entropy calculation successful")

            cls.findMaxGainFeature()
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
                    cls.partitionCount += 1

            cls.classNames = [None] * cls.partitionCount
            cls.classData = [ [ None for i in range(cls.instanceCount) ] for j in range(cls.partitionCount) ]
            cls.classCount = [None] * cls.partitionCount
            j = 0
            
            for line in lines:
                line = line.rstrip()
                values = line.split(" ")
                cls.classNames[j] = values[0]
                cls.classCount[j] = 0
                i = 0
                while i < len(values)-1:
                    cls.classCount[j] += 1
                    cls.classData[j][i] = int(values[i + 1])
                    i += 1
                j += 1
            
        except Exception as ex:
            print("Partition file not found.")
            traceback.print_exc()

    @classmethod
    def parseDataset(cls, fileName):
        print(fileName)
        try:
            with open(fileName) as file_object:
                line = file_object.readline().rstrip()
                countString = line.split(" ")
                cls.instanceCount = int(countString[0])
                cls.featureCount = int(countString[1])
                cls.inputData = [ [ None for i in range(cls.featureCount) ] for j in range(cls.instanceCount) ]
                rowCount = 0

            with open(fileName) as fp:
                line = fp.readline().rstrip()
                line = fp.readline().rstrip()
                while line:
                    features = line.split(" ")
                    i = 0
                    while i<len(features):
                        cls.inputData[rowCount][i] = int(features[i])
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
            while i < cls.partitionCount:
                if i == cls.splitClassID:
                    split1 = cls.classNames[i] + "0"
                    split2 = cls.classNames[i] + "1"
                    split3 = cls.classNames[i] + "2"
                    j = 0
                    while j < cls.classCount[i]:
                        if cls.inputData[cls.classData[i][j] - 1][cls.splitFeatureID] == 1:
                            split1 = str(split1) + " " + str(cls.classData[i][j])
                        if cls.inputData[cls.classData[i][j] - 1][cls.splitFeatureID] == 0:
                            split2 = str(split2) + " " + str(cls.classData[i][j])
                        if cls.inputData[cls.classData[i][j] - 1][cls.splitFeatureID] == 2:
                            split3 = str(split3) + " " + str(cls.classData[i][j])
                        j += 1
                    output.write(str(split1))
                    output.write("\n")
                    output.write(str(split2))
                    output.write("\n")
                    output.write(str(split3))
                    if i < cls.partitionCount:
                        output.write("\n")
                    print("Partition ", cls.classNames[i], " was replaced with partitions ", cls.classNames[i], "0", ",", cls.classNames[i], "1" , " using Feature " , (cls.splitFeatureID + 1))
                else:
                    line = cls.classNames[i]
                    j = 0
                    while j < cls.classCount[i]:
                        line = str(line) + " " + str(cls.classData[i][j])
                        j += 1
                    output.write(str(line))
                    if i < cls.partitionCount:
                        output.write("\n")
                i += 1
            output.close() 
        except IOError as e:
            traceback.print_exc()


if __name__ == '__main__':
    import sys
    IDthree.main(sys.argv)