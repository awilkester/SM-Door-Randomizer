import miscFunctions
import hexMethods
import operator

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
