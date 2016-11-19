import miscFunctions
import hexMethods
import operator
import random
import os

headerSize = int("0x200",0)

HEX_FILTER = "0123456789ABCDEFabcdefx"
NUM_FILTER = "0123456789"

# directions
DIRECTION = ["LEFT","RIGHT","UP","DOWN","LEFT","RIGHT","UP","DOWN"]

# sort a file by a given column
def sort(fileName,index,tie):
    roomArray = miscFunctions.importList(fileName,
                                         [HEX_FILTER,
                                          HEX_FILTER,
                                          HEX_FILTER,
                                          HEX_FILTER])
    roomArray = sorted(roomArray, key=operator.itemgetter(index,tie))
    data = open(fileName,"w")
    for i in roomArray:
        data.write(i[0] + "\t"
                   + i[1] + "\t"
                   + i[2] + "\t"
                   + i[3] + "\n")

    data.close()

# print a list of doors
def printDoors():
    roomArray = miscFunctions.importList("doorlist.txt",
                                         [HEX_FILTER,
                                          HEX_FILTER,
                                          NUM_FILTER])
    # print roomArray
    data = open("doors.txt","w")
    dataLeft = open("doors-left.txt","w")
    dataRight = open("doors-right.txt","w")
    dataUp = open("doors-up.txt","w")
    dataDown = open("doors-down.txt","w")

    for i in roomArray:
        # get door pointer
        doorArrayPointer = hex(int("0x70000",0)
                               + int("0x" + i[1],0)
                               + headerSize)

        for j in range(0,int(i[2])+1):
            doorPointer = hexMethods.getHalfword("clean-rom.smc",
                                                 hex(int(doorArrayPointer,0)
                                                     + 2*j))
            doorPointer2 = hex(int(doorPointer,0) + headerSize + int("0x10000",0))
            destPointer = hexMethods.getHalfword("clean-rom.smc",
                                                 hex(int(doorPointer2,0)))
            #destPointer = hex(int("0x70000",0)
            #                   + int(destPointer,0)
            #                   + headerSize)
            direction = hexMethods.getByte("clean-rom.smc",
                                           hex(int(doorPointer2,0) + 3))
            
            # write the following data:
            # pointer to door
            # pointer to the door array source
            # pointer to room
            # room door goes to
            # door direction
            if int(direction,0) < 8:
                direction = DIRECTION[int(direction,0)]
                data.write(doorPointer
                           + "\t" + hex(int(doorArrayPointer,0) + 2*j)
                           + "\t0x" + i[0]
                           + "\t" + destPointer
                           + "\t" + direction
                           + "\n")
                if direction is "UP":
                    dataUp.write(doorPointer
                                 + "\t" + hex(int(doorArrayPointer,0) + 2*j)
                                 + "\t0x" + i[0]
                                 + "\t" + destPointer
                                 + "\n")
                if direction is "DOWN":
                    dataDown.write(doorPointer
                                   + "\t" + hex(int(doorArrayPointer,0) + 2*j)
                                   + "\t0x" + i[0]
                                   + "\t" + destPointer
                                   + "\n")
                if direction is "LEFT":
                    dataLeft.write(doorPointer
                                   + "\t" + hex(int(doorArrayPointer,0) + 2*j)
                                   + "\t0x" + i[0]
                                   + "\t" + destPointer
                                   + "\n")
                if direction is "RIGHT":
                    dataRight.write(doorPointer
                                    + "\t" + hex(int(doorArrayPointer,0) + 2*j)
                                    + "\t0x" + i[0]
                                    + "\t" + destPointer
                                    + "\n")
            else:
                data.write(doorPointer
                           + "\t" + hex(int(doorArrayPointer,0) + 2*j)
                           + "\t0x" + i[0]
                           + "\t" + destPointer
                           + "\t" + direction
                           + "\n")
        

    data.close()
    dataUp.close()
    dataDown.close()
    dataLeft.close()
    dataRight.close()
    sort("doors-right.txt",3,2)
    sort("doors-up.txt",3,2)
    sort("doors-left.txt",2,3)
    sort("doors-down.txt",2,3)

# swaps doors at random.
def swapDoors(source,fileName,seed,easy=True,perc=100):
    # initialize seed
    random.seed(seed)

    # create new file
    data = open(source,"rb")
    dest = open(fileName,"wb")
    dest.write(data.read())
    dest.close()
    data.close()
    
    # read door lists
    leftDoorArray = miscFunctions.importList("doors-left.txt",
                                             [HEX_FILTER,HEX_FILTER])
    rightDoorArray = miscFunctions.importList("doors-right.txt",
                                              [HEX_FILTER,HEX_FILTER])
    upDoorArray = miscFunctions.importList("doors-up.txt",
                                           [HEX_FILTER,HEX_FILTER])
    downDoorArray = miscFunctions.importList("doors-down.txt",
                                             [HEX_FILTER,HEX_FILTER])

    if perc != 100:
        # filter a sublist
        leftCount = len(leftDoorArray)
        shuffleArray = permuteList(leftCount)
        shuffleArray = shuffleArray[:(leftCount*perc/100)]
        leftDoorArray = percolate(leftDoorArray,shuffleArray)
        rightDoorArray = percolate(rightDoorArray,shuffleArray)

        # filter a sublist
        downCount = len(downDoorArray)
        shuffleArray = permuteList(downCount)
        shuffleArray = shuffleArray[:(downCount*perc/100)]
        downDoorArray = percolate(downDoorArray,shuffleArray)
        upDoorArray = percolate(upDoorArray,shuffleArray)
        

    swapDoorList(fileName,leftDoorArray,rightDoorArray,easy)
    swapDoorList(fileName,upDoorArray,downDoorArray,easy)

# swaps doors at a local level
def swapDoorsLocal(source,fileName,seed,easy = True,perc=100):
    # initialize seed + debug message.
    random.seed(seed)

    # create new file
    data = open(source,"rb")
    dest = open(fileName,"wb")
    dest.write(data.read())
    dest.close()
    data.close()

    locaArray1 = ["brinstar",
                  "crateria",
                  "maridia",
                  "norfair",
                  "wreck"]

    locaArray2 = ["itemsA",
                  "itemsB",
                  "lower",]
    
    folder = "local-data/doors-"
    
    # read doors by location (up/down and left right)
    for i in locaArray1:
        leftDoorArray = miscFunctions.importList(folder + i + "-left.txt",
                                                 [HEX_FILTER,HEX_FILTER])
        rightDoorArray = miscFunctions.importList(folder + i + "-right.txt",
                                                  [HEX_FILTER,HEX_FILTER])
        downDoorArray = miscFunctions.importList(folder + i + "-down.txt",
                                                 [HEX_FILTER,HEX_FILTER])
        upDoorArray = miscFunctions.importList(folder + i + "-up.txt",
                                               [HEX_FILTER,HEX_FILTER])

        if perc != 100:
            # filter a sublist
            leftCount = len(leftDoorArray)
            shuffleArray = permuteList(leftCount)
            shuffleArray = shuffleArray[:(leftCount*perc/100)]
            leftDoorArray = percolate(leftDoorArray,shuffleArray)
            rightDoorArray = percolate(rightDoorArray,shuffleArray)

            # filter a sublist
            downCount = len(downDoorArray)
            shuffleArray = permuteList(downCount)
            shuffleArray = shuffleArray[:(downCount*perc/100)]
            downDoorArray = percolate(downDoorArray,shuffleArray)
            upDoorArray = percolate(upDoorArray,shuffleArray)
        

        swapDoorList(fileName,leftDoorArray,rightDoorArray,easy)
        swapDoorList(fileName,upDoorArray,downDoorArray,easy)

    # read doors by location (left right only)
    for i in locaArray2:
        leftDoorArray = miscFunctions.importList(folder + i + "-left.txt",
                                                 [HEX_FILTER,HEX_FILTER])
        rightDoorArray = miscFunctions.importList(folder + i + "-right.txt",
                                                  [HEX_FILTER,HEX_FILTER])

        if perc != 100:
            # filter a sublist
            leftCount = len(leftDoorArray)
            shuffleArray = permuteList(leftCount)
            shuffleArray = shuffleArray[:(leftCount*perc/100)]
            leftDoorArray = percolate(leftDoorArray,shuffleArray)
            rightDoorArray = percolate(rightDoorArray,shuffleArray)
        
        swapDoorList(fileName,leftDoorArray,rightDoorArray,easy)

# swaps the contents of two door arrays using permutation.
# arrays must have the same length.
def swapDoorList(fileName,doorList1,doorList2,easy = True):
    # create permutation
    swapArray = permuteList(len(doorList1))
    
    # swap all pairs according to the following rule:
    # index i is swapped with array[i]
    for i in range(0,len(doorList1)):
        A1offset = doorList1[i][1]
        A2offset = doorList1[swapArray[i]][1]
        B1offset = doorList2[i][1]
        B2offset = doorList2[swapArray[i]][1]
        DoorA1 = hexMethods.getRawBytes(fileName,A1offset,2)
        DoorA2 = hexMethods.getRawBytes(fileName,A2offset,2)
        DoorB1 = hexMethods.getRawBytes(fileName,B1offset,2)
        DoorB2 = hexMethods.getRawBytes(fileName,B2offset,2)

        hexMethods.writeRawBytes(fileName,A1offset,DoorA2,2)
        hexMethods.writeRawBytes(fileName,A2offset,DoorA1,2)
        hexMethods.writeRawBytes(fileName,B1offset,DoorB2,2)
        hexMethods.writeRawBytes(fileName,B2offset,DoorB1,2)

        # update references
        if easy:
            temp1 = doorList2[i]
            temp2 = doorList2[swapArray[i]]
            doorList2[i] = temp2
            doorList2[swapArray[i]] = temp1

# given a list of indices, returns the subarray of the given array
# with the specified indices in the given order.
def percolate(array,indexList):
    newArray = []
    for i in indexList:
        newArray.append(array[i])
    return newArray

# create permutation
def permuteList(size):
    swapArray = []
    for i in range(0,size):
        swapArray.append(i)
    random.shuffle(swapArray)
    return swapArray

# not used, just outputs which doors lead into a given room set.
# filename is a door list
# surveyname is a list of rooms
def survey(filename,surveyname):
    surveyList = miscFunctions.importList(surveyname,[HEX_FILTER])
    fileList = miscFunctions.importList(filename,[HEX_FILTER,
                                                  HEX_FILTER,
                                                  HEX_FILTER,
                                                  HEX_FILTER])

    for i in range(0,len(surveyList)):
        surveyList[i] = int("0x" + surveyList[i],16)

    for i in range(0,len(fileList)):
        if int(fileList[i][2],0) in surveyList:
            print i+1
        elif int(fileList[i][3],0) + int("0x70000",0) in surveyList:
            print i+1
    

def main():
    print "Welcome to the Super Metroid Door Randomizer."
    print "This application randomizes the rooms that each door leads to."
    print "For additional information, type h at any step of the process."
    print "--------------"

    currInput = 0
    while(currInput != "1" and currInput != "2"):
        print "Pick your randomization type. (Type 1 or 2)"
        print "1. Global"
        print "2. Local"
        currInput = raw_input("-> ")
        if currInput == "h":
            print "Global randomization will shuffle all rooms, regardless of location."
            print "Local randomization will only shuffle rooms locally."
            print "This means that rooms belong to Brinstar, e.g., will connect to"
            print "other rooms in Brinstar."
            print "Rooms that cross two regions will be untouched."
            print "Item/Save/Recharge rooms are considered their own type."
            print "Note: Global randomization is not perfectly working yet."
    if currInput == "1":
        globalType = True
    else:
        globalType = False

    currInput = 0
    while(currInput != "1" and currInput != "2"):
        print "Backtracking enabled? (Type 1 or 2)"
        print "1. Yes"
        print "2. No"
        currInput = raw_input("-> ")
        if currInput == "h":
            print "If backtracking is disabled, backtracking through a door"
            print "will not return you to the room you came from."
    if currInput == "1":
        easyMode = True
    else:
        easyMode = False

    currInput = 0
    while(currInput not in ["1","2","3","4","5","6","7","8","9","10"]):
        print "Pick your randomization level."
        print "1. 10%"
        print "2. 20%"
        print "3. 30%"
        print "4. 40%"
        print "5. 50%"
        print "6. 60%"
        print "7. 70%"
        print "8. 80%"
        print "9. 90%"
        print "10. 100%"
        currInput = raw_input("-> ")
        if currInput == "h":
            print "The randomization level will determine how many doors"
            print "are shuffled. Higher percentages mean more doors."
    percentage = int(currInput)*10

    currInput = ""
    while(currInput == ""):
        print "Type the filename of the clean rom to reference:"
        print "(This file should be in the same folder as the executable.)"
        currInput = raw_input("-> ")
    source = currInput

    currInput = ""
    while(currInput == ""):
        print "Type the filename to output to:"
        currInput = raw_input("-> ")
    output = currInput

    currInput = ""
    while(currInput == ""):
        print "Type a seed. (This can be anything.)"
        currInput = raw_input("-> ")
    seed = currInput

    print "processing ROM..."
    if globalType:
        swapDoors(source,output,seed,easyMode)
    else:
        swapDoorsLocal(source,output,seed,easyMode)
    print "Done! Reminder: The morph ball, the missiles nearby"
    print "and the bombs are always fixed."
    print "So is Ceres Station and Tourian."

    os.system("pause")
    

if __name__ == "__main__":
    main()
