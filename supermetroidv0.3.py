import miscFunctions
import hexMethods
import operator
import random
import os

HEX_FILTER = "0123456789ABCDEFabcdefx"
NUM_FILTER = "0123456789"

def detectHeader(source):
    header = 0
    byte10 = int(hexMethods.getByte(source,hex(header+10)),0)
    byte11 = int(hexMethods.getByte(source,hex(header+11)),0)
    byte12 = int(hexMethods.getByte(source,hex(header+12)),0)
    byte13 = int(hexMethods.getByte(source,hex(header+13)),0)
    # start of ROM + 10 bytes should be the sequence a3,02,85,04
    while byte10 != 163 or byte11 != 2 or byte12 != 133 or byte13 != 4:
        header += 1
        byte10 = int(hexMethods.getByte(source,hex(header+10)),0)
        byte11 = int(hexMethods.getByte(source,hex(header+11)),0)
        byte12 = int(hexMethods.getByte(source,hex(header+12)),0)
        byte13 = int(hexMethods.getByte(source,hex(header+13)),0)
    return header

# verifies that a seed is valid.
def seedChecksum(seed):
    # constants
    globHorz = 222
    globVert = 26
    brinHorz = 38
    brinVert = 2
    cratHorz = 20
    cratVert = 3
    iteAHorz = 20
    iteBHorz = 24
    lownHorz = 14
    mariHorz = 34
    mariVert = 11
    norfHorz = 48
    norfVert = 6
    wrecHorz = 10
    wrecVert = 2
    
    seedArray = seed.split("_")
    if len(seedArray) < 2:
        return False,"What."
    if seedArray[0] != "v0.2":
        return False,"Version"
    
    # global settings checksum
    if seedArray[1] == "gb" or seedArray[1] == "g":
        
        # determine if 100% randomization was used
        if seedArray[2] == "p":
            # 5 pieces of data for global settings with 100% randomization
            if len(seedArray) != 5:
                return False,"Data size mismatch."
            
            # assert the horizontal shuffle array is valid
            hShufArray = []
            # check the array string is the correct length
            if len(seedArray[3]) != 2*globHorz:
                return False,"Horizontal map string mismatch."
            # convert array, make sure each entry is hexadecimal
            for i in range(globHorz):
                try: currDoor = int(seedArray[3][2*i:2*i+2],16)
                except ValueError: return False,"Horizontal map string corrupted."
                # check the entry is a valid ID
                if currDoor >= globHorz:
                    return False,"Invalid horizontal map ID found."
                hShufArray.append(currDoor)
            # check every entry is unique
            hShufArray.sort()
            for i in range(globHorz-1):
                if hShufArray[i] == hShufArray[i+1]:
                    return False,"Duplicate horizontal map ID found."

            # assert the vertical shuffle array is valid
            vShufArray = []
            # check the array string is the correct length
            if len(seedArray[4]) != 2*globVert:
                return False,"Vertical map string mismatch."
            # convert array, make sure each entry is hexadecimal
            for i in range(globVert):
                try: currDoor = int(seedArray[4][2*i:2*i+2],16)
                except ValueError: return False,"Vertical map string corrupted."
                # check the entry is a valid ID
                if currDoor >= globVert:
                    return False,"Invalid vertical map ID found."
                vShufArray.append(currDoor)
            # check every entry is unique
            vShufArray.sort()
            for i in range(globVert-1):
                if vShufArray[i] == vShufArray[i+1]:
                    return False,"Duplicate vertical map ID found."
            return True,""
        else:
            # 8 pieces of data for global settings with <100% randomization.
            if len(seedArray) != 8:
                return False,"Data size mismatch."
        
            # assert the horizontal door array is valid
            horzArray = []
            try: horzSize = int(seedArray[2],16)
            except ValueError: return False,"Horizontal array size corrupted."
            # check the number of doors is correct
            if horzSize > globHorz:
                return False,"Too many horizontal doors."
            # check the array string is the correct length
            if len(seedArray[3]) != 2*horzSize:
                return False,"Horizontal doors string mismatch."
            # convert array, make sure each entry is hexadecimal
            for i in range(horzSize):
                try: currDoor = int(seedArray[3][2*i:2*i+2],16)
                except ValueError: return False,"Horizontal doors string corrupted."
                # check the entry is a valid ID
                if currDoor >= globHorz:
                    return False,"Invalid horizontal door ID found."
                horzArray.append(currDoor)
            # check every entry is unique
            horzArray.sort()
            for i in range(horzSize-1):
                if horzArray[i] == horzArray[i+1]:
                    return False,"Duplicate horizontal door ID found."

            # assert the vertical door array is valid
            vertArray = []
            try: vertSize = int(seedArray[4],16)
            except ValueError: return False,"Vertical array size corrupted."
            # check the number of doors is correct
            if vertSize > globVert:
                return False,"Too many vertical doors."
            # check the array string is the correct length
            if len(seedArray[5]) != 2*vertSize:
                return False,"Vertical doors string mismatch."
            # convert array, make sure each entry is hexadecimal
            for i in range(vertSize):
                try: currDoor = int(seedArray[5][2*i:2*i+2],16)
                except ValueError: return False,"Vertical doors string corrupted."
                # check the entry is a valid ID
                if currDoor >= globVert:
                    return False,"Invalid vertical door ID found."
                vertArray.append(currDoor)
            # check every entry is unique
            vertArray.sort()
            for i in range(vertSize-1):
                if vertArray[i] == vertArray[i+1]:
                    return False,"Duplicate vertical door ID found."

            # assert the horizontal shuffle array is valid
            hShufArray = []
            # check the array string is the correct length
            if len(seedArray[6]) != 2*horzSize:
                return False,"Horizontal map string mismatch."
            # convert array, make sure each entry is hexadecimal
            for i in range(horzSize):
                try: currDoor = int(seedArray[6][2*i:2*i+2],16)
                except ValueError: return False,"Horizontal map string corrupted."
                # check the entry is a valid ID
                if currDoor >= horzSize:
                    return False,"Invalid horizontal map ID found."
                hShufArray.append(currDoor)
            # check every entry is unique
            hShufArray.sort()
            for i in range(horzSize-1):
                if hShufArray[i] == hShufArray[i+1]:
                    return False,"Duplicate horizontal map ID found."

            # assert the vertical shuffle array is valid
            vShufArray = []
            # check the array string is the correct length
            if len(seedArray[7]) != 2*vertSize:
                return False,"Vertical map string mismatch."
            # convert array, make sure each entry is hexadecimal
            for i in range(vertSize):
                try: currDoor = int(seedArray[7][2*i:2*i+2],16)
                except ValueError: return False,"Vertical map string corrupted."
                # check the entry is a valid ID
                if currDoor >= vertSize:
                    return False,"Invalid vertical map ID found."
                vShufArray.append(currDoor)
            # check every entry is unique
            vShufArray.sort()
            for i in range(vertSize-1):
                if vShufArray[i] == vShufArray[i+1]:
                    return False,"Duplicate vertical map ID found."

            return True,""
        
    # local case
    if seedArray[1] == "lb" or seedArray[1] == "l":
        # verify bitflag
        bitflag = int(seedArray[2],16)
        if int(seedArray[2],16) > int("0x100",0):
            return False,"bitflag mismatch."

        # check flags and record number of 100%s.
        percArray = []
        flag = int("0x80",0)
        for i in range(8):
            percArray.append(not (bitflag&flag == 0))
            flag = flag>>1

        # the number of array entries is given by
        # 3 for the version number, randomization type, and bitflag
        # each 100% adds an array size and an array for each direction
        # 5 horz/vert types and 2 horz only types
        # 2 shuffle types
        arraySize = 3
        for i in range(8):
            if percArray[i]:
                # general case: 2 shuffle arrays
                if i < 5:
                    arraySize += 2
                # no vertical doors case
                else:
                    arraySize += 1
            else:
                # general case: 2 shuffle arrays
                # + 4 pieces of data for room arrays
                if i < 5:
                    arraySize += 4 + 2
                # no vertical doors case
                else:
                    arraySize += 2 + 1

        if len(seedArray) != arraySize:
            return False,"Data size mismatch."

        currIndex = 3
        # check that each array is handled correctly
        array = [[brinHorz,brinVert],
                 [cratHorz,cratVert],
                 [mariHorz,mariVert],
                 [norfHorz,norfVert],
                 [wrecHorz,wrecVert],
                 [iteAHorz,0],
                 [iteBHorz,0],
                 [lownHorz,0],]
        areaIDarray = ["Brinstar",
                       "Crateria",
                       "Maridia",
                       "Norfair",
                       "Wrecked Ship",
                       "Item Rooms A",
                       "Item Rooms B",
                       "Lower Norfair",]
        for i in range(8):
            if percArray[i]:
                # 100% case
                # assert the horizontal shuffle array is valid
                hShufArray = []
                # check the array string is the correct length
                if len(seedArray[currIndex+0]) != 2*array[i][0]:
                    return False,areaIDarray[i] + " horizontal map string mismatch."
                # convert array, make sure each entry is hexadecimal
                for j in range(array[i][0]):
                    try: currDoor = int(seedArray[currIndex+0][2*j:2*j+2],16)
                    except ValueError: return False,areaIDarray[i] + " horizontal map string corrupted."
                    # check the entry is a valid ID
                    if currDoor >= array[i][0]:
                        return False,areaIDarray[i] + " invalid horizontal map ID found."
                    hShufArray.append(currDoor)
                # check every entry is unique
                hShufArray.sort()
                for j in range(array[i][0]-1):
                    if hShufArray[j] == hShufArray[j+1]:
                        return False,areaIDarray[i] + " duplicate horizontal map ID found."
                currIndex += 1

                # only do vertical checks for index 0-4
                if i < 5:
                    # assert the vertical shuffle array is valid
                    vShufArray = []
                    # check the array string is the correct length
                    if len(seedArray[currIndex]) != 2*array[i][1]:
                        return False,areaIDarray[i] + " vertical map string mismatch."
                    # convert array, make sure each entry is hexadecimal
                    for j in range(array[i][1]):
                        try: currDoor = int(seedArray[currIndex][2*j:2*j+2],16)
                        except ValueError: return False,areaIDarray[i] + " vertical map string corrupted."
                        # check the entry is a valid ID
                        if currDoor >= array[i][1]:
                            return False,areaIDarray[i] + " invalid vertical map ID found."
                        vShufArray.append(currDoor)
                    # check every entry is unique
                    vShufArray.sort()
                    for j in range(array[i][1]-1):
                        if vShufArray[j] == vShufArray[j+1]:
                            return False,areaIDarray[i] + " duplicate vertical map ID found."
                    currIndex += 1
                    
            else:
                # not 100% case
                # assert the horizontal door array is valid
                horzArray = []
                try: horzSize = int(seedArray[currIndex],16)
                except ValueError: return False,areaIDarray[i] + " horizontal array size corrupted."
                # check the number of doors is correct
                if horzSize > array[i][0]:
                    return False,areaIDarray[i] + " too many horizontal doors."
                # check the array string is the correct length
                if len(seedArray[currIndex+1]) != 2*horzSize:
                    return False,areaIDarray[i] + " horizontal doors string mismatch."
                # convert array, make sure each entry is hexadecimal
                for j in range(horzSize):
                    try: currDoor = int(seedArray[currIndex+1][2*j:2*j+2],16)
                    except ValueError: return False,areaIDarray[i] + " horizontal doors string corrupted."
                    # check the entry is a valid ID
                    if currDoor >= array[i][0]:
                        return False,areaIDarray[i] + " invalid horizontal door ID found."
                    horzArray.append(currDoor)
                # check every entry is unique
                horzArray.sort()
                for j in range(horzSize-1):
                    if horzArray[j] == horzArray[j+1]:
                        return False,areaIDarray[i] + " duplicate horizontal door ID found."
                currIndex += 2

                # only handle vertical case for index 0-4
                if i < 5:
                    # assert the vertical door array is valid
                    vertArray = []
                    try: vertSize = int(seedArray[currIndex],16)
                    except ValueError: return False,areaIDarray[i] + " vertical array size corrupted."
                    # check the number of doors is correct
                    if vertSize > array[i][1]:
                        return False,areaIDarray[i] + " too many vertical doors."
                    # check the array string is the correct length
                    if len(seedArray[currIndex+1]) != 2*vertSize:
                        return False,areaIDarray[i] + " vertical doors string mismatch."
                    # convert array, make sure each entry is hexadecimal
                    for j in range(vertSize):
                        try: currDoor = int(seedArray[currIndex+1][2*j:2*j+2],16)
                        except ValueError: return False,areaIDarray[i] + " vertical doors string corrupted."
                        # check the entry is a valid ID
                        if currDoor >= array[i][1]:
                            return False,areaIDarray[i] + " invalid vertical door ID found."
                        vertArray.append(currDoor)
                    # check every entry is unique
                    vertArray.sort()
                    for j in range(vertSize-1):
                        if vertArray[j] == vertArray[j+1]:
                            return False,areaIDarray[i] + " duplicate vertical door ID found."
                    currIndex += 2

                # assert the horizontal shuffle array is valid
                hShufArray = []
                # check the array string is the correct length
                if len(seedArray[currIndex]) != 2*horzSize:
                    return False,areaIDarray[i] + " horizontal map string mismatch."
                # convert array, make sure each entry is hexadecimal
                for j in range(horzSize):
                    try: currDoor = int(seedArray[currIndex][2*j:2*j+2],16)
                    except ValueError: return False,areaIDarray[i] + " horizontal map string corrupted."
                    # check the entry is a valid ID
                    if currDoor >= array[i][0]:
                        return False,areaIDarray[i] + " invalid horizontal map ID found."
                    hShufArray.append(currDoor)
                # check every entry is unique
                hShufArray.sort()
                for j in range(horzSize-1):
                    if hShufArray[j] == hShufArray[j+1]:
                        return False,areaIDarray[i] + " duplicate horizontal map ID found."
                currIndex += 1

                if i < 5:
                    # assert the vertical shuffle array is valid
                    vShufArray = []
                    # check the array string is the correct length
                    if len(seedArray[currIndex]) != 2*vertSize:
                        return False,areaIDarray[i] + " vertical map string mismatch."
                    # convert array, make sure each entry is hexadecimal
                    for j in range(vertSize):
                        try: currDoor = int(seedArray[currIndex][2*j:2*j+2],16)
                        except ValueError: return False,areaIDarray[i] + " vertical map string corrupted."
                        # check the entry is a valid ID
                        if currDoor >= array[i][1]:
                            return False,areaIDarray[i] + " invalid vertical map ID found."
                        vShufArray.append(currDoor)
                    # check every entry is unique
                    vShufArray.sort()
                    for j in range(vertSize-1):
                        if vShufArray[j] == vShufArray[j+1]:
                            return False,areaIDarray[i] + " duplicate vertical map ID found."
                    currIndex += 1
        return True,""
    return False,"Invalid randomization type."

# swaps doors using a premade seed.
def swapDoorsSeed(source,fileName,seed):
    # constants
    globHorz = 222
    globVert = 26
    brinHorz = 38
    brinVert = 2
    cratHorz = 20
    cratVert = 3
    iteAHorz = 20
    iteBHorz = 24
    lownHorz = 14
    mariHorz = 34
    mariVert = 11
    norfHorz = 48
    norfVert = 6
    wrecHorz = 10
    wrecVert = 2

    # create new file
    headerSize = detectHeader(source)
    data = open(source,"rb")
    dest = open(fileName,"wb")
    # the entire system assumes the ROM has 0x200 bytes of header (wups)
    if headerSize < int("0x200",0):
        for i in range(int("0x200",0) - headerSize):
            dest.write("\0")
        dest.write(data.read())
    else:
        dest.write(data.read()[headerSize-int("0x200",0):])
    dest.close()
    data.close()
    
    seedArray = seed.split("_")
    # backtracking is on if the ID is "Xb"
    easy = (len(seedArray[1]) == 2)
        
    if seedArray[1] == "gb" or seedArray[1] == "g":

        # create door lists
        leftDoorArray = miscFunctions.importList("doors-left.txt",
                                                 [HEX_FILTER,HEX_FILTER])
        rightDoorArray = miscFunctions.importList("doors-right.txt",
                                                  [HEX_FILTER,HEX_FILTER])
        upDoorArray = miscFunctions.importList("doors-up.txt",
                                               [HEX_FILTER,HEX_FILTER])
        downDoorArray = miscFunctions.importList("doors-down.txt",
                                                 [HEX_FILTER,HEX_FILTER])
        
        # determine if 100% randomization was used
        if seedArray[2] == "p":
            
            # generate the horizontal shuffle array
            hShufArray = []
            for i in range(globHorz):
                currDoor = int(seedArray[3][2*i:2*i+2],16)
                hShufArray.append(currDoor)

            # generate the vertical shuffle array
            vShufArray = []
            for i in range(globVert):
                currDoor = int(seedArray[4][2*i:2*i+2],16)
                vShufArray.append(currDoor)
        else:
            # generate horizontal percolation array
            horzArray = []
            horzSize = int(seedArray[2],16)
            for i in range(horzSize):
                currDoor = int(seedArray[3][2*i:2*i+2],16)
                horzArray.append(currDoor)
            leftDoorArray = percolate(leftDoorArray,horzArray)
            rightDoorArray = percolate(rightDoorArray,horzArray)
            
            # generate vertical percolation array
            vertArray = []
            vertSize = int(seedArray[4],16)
            for i in range(vertSize):
                currDoor = int(seedArray[5][2*i:2*i+2],16)
                vertArray.append(currDoor)
            downDoorArray = percolate(downDoorArray,vertArray)
            upDoorArray = percolate(upDoorArray,vertArray)
            
            # geerate the horizontal shuffle array
            hShufArray = []
            for i in range(horzSize):
                currDoor = int(seedArray[6][2*i:2*i+2],16)
                hShufArray.append(currDoor)
            
            # generate the vertical shuffle array is valid
            vShufArray = []
            # convert array, make sure each entry is hexadecimal
            for i in range(vertSize):
                currDoor = int(seedArray[7][2*i:2*i+2],16)
                vShufArray.append(currDoor)

        # create ROM!!!
        swapArray = swapDoorListSeed(fileName,leftDoorArray,rightDoorArray,hShufArray,easy)
        swapArray = swapDoorListSeed(fileName,upDoorArray,downDoorArray,vShufArray,easy)
        
    # local case
    if seedArray[1] == "lb" or seedArray[1] == "l":
        # check flags and record number of 100%s.
        bitflag = int(seedArray[2],16)
        percArray = []
        flag = int("0x80",0)
        for i in range(8):
            percArray.append(not (bitflag&flag == 0))
            flag = flag>>1

        currIndex = 3
        # check that each array is handled correctly
        array = [[brinHorz,brinVert],
                 [cratHorz,cratVert],
                 [mariHorz,mariVert],
                 [norfHorz,norfVert],
                 [wrecHorz,wrecVert],
                 [iteAHorz,0],
                 [iteBHorz,0],
                 [lownHorz,0],]
        areaIDarray = ["brinstar",
                       "crateria",
                       "maridia",
                       "norfair",
                       "wreck",
                       "itemsA",
                       "itemsB",
                       "lower",]
        folder = "local-data/doors-"
        for i in range(8):
            name = areaIDarray[i]
            leftDoorArray = miscFunctions.importList(folder + name + "-left.txt",
                                                     [HEX_FILTER,HEX_FILTER])
            rightDoorArray = miscFunctions.importList(folder + name + "-right.txt",
                                                      [HEX_FILTER,HEX_FILTER])
            if i < 5:
                downDoorArray = miscFunctions.importList(folder + name + "-down.txt",
                                                         [HEX_FILTER,HEX_FILTER])
                upDoorArray = miscFunctions.importList(folder + name + "-up.txt",
                                                       [HEX_FILTER,HEX_FILTER])
            
            if percArray[i]:
                # 100% case
                # generate the horizontal shuffle array
                hShufArray = []
                for j in range(array[i][0]):
                    currDoor = int(seedArray[currIndex+0][2*j:2*j+2],16)
                    hShufArray.append(currDoor)
                currIndex += 1

                # only do vertical shuffles for index 0-4
                if i < 5:
                    # assert the vertical shuffle array is valid
                    vShufArray = []
                    for j in range(array[i][1]):
                        currDoor = int(seedArray[currIndex][2*j:2*j+2],16)
                        vShufArray.append(currDoor)
                    currIndex += 1
                    
            else:
                # not 100% case
                # generate the horizontal percolation array
                horzArray = []
                horzSize = int(seedArray[currIndex],16)
                for j in range(horzSize):
                    currDoor = int(seedArray[currIndex+1][2*j:2*j+2],16)
                    horzArray.append(currDoor)
                currIndex += 2
                leftDoorArray = percolate(leftDoorArray,horzArray)
                rightDoorArray = percolate(rightDoorArray,horzArray)

                # only handle vertical case for index 0-4
                if i < 5:
                    # generate the vertical percolation array
                    vertArray = []
                    vertSize = int(seedArray[currIndex],16)
                    for j in range(vertSize):
                        currDoor = int(seedArray[currIndex+1][2*j:2*j+2],16)
                        vertArray.append(currDoor)
                    currIndex += 2
                    downDoorArray = percolate(downDoorArray,vertArray)
                    upDoorArray = percolate(upDoorArray,vertArray)

                # generate the horizontal shuffle array
                hShufArray = []
                for j in range(horzSize):
                    currDoor = int(seedArray[currIndex][2*j:2*j+2],16)
                    hShufArray.append(currDoor)
                currIndex += 1

                if i < 5:
                    # generate the vertical shuffle array
                    vShufArray = []
                    for j in range(vertSize):
                        currDoor = int(seedArray[currIndex][2*j:2*j+2],16)
                        vShufArray.append(currDoor)
                    currIndex += 1

            # create ROM!!!
            # 3 cases: item rooms, lower norfair and other
            if i < 5:
                swapArray = swapDoorListSeed(fileName,leftDoorArray,rightDoorArray,hShufArray,easy)
                swapArray = swapDoorListSeed(fileName,upDoorArray,downDoorArray,vShufArray,easy)
            elif i == 5 or i == 6:
                swapArray = swapDoorListSeed(fileName,leftDoorArray,rightDoorArray,hShufArray,True)
            else:
                swapArray = swapDoorListSeed(fileName,leftDoorArray,rightDoorArray,hShufArray,easy)

    # remove the 0x200 header bytes.
    data = open(fileName,"rb")
    romData = data.read()[int("0x200",0):]
    data.close()
    dest = open(fileName,"wb")
    dest.write(romData)
    dest.close()

# swap items at random.
# assumes the doors have already been swapped and a output file was created.
def swapItems(fileName,seed,itemRandom,itemFull,itemETank,itemMiss,itemSMiss,itemPBomb,itemCount):
    # initialize seed
    random.seed(seed)

    ETANK = 0
    MISSILE = 1
    SMISSILE = 2
    PBOMB = 3
    CHARGE = 5
    ICE = 6
    HIJUMP = 7
    SPEED = 8
    WAVE = 9
    SPAZER = 10
    SPRING = 11
    VARIA = 12
    GRAVITY = 13
    XRAY = 14
    PLASMA = 15
    GRAPPLE = 16
    SPACE = 17
    SCREW = 18
    RESERVE = 20
    # debug
    stringArray = ["E-Tank",
                   "Missile",
                   "Super",
                   "Power Bomb",
                   "Bombs",
                   "Charge",
                   "Ice",
                   "Hi Jump",
                   "Speed Booster",
                   "Wave Beam",
                   "Spazer",
                   "Spring Ball",
                   "Varia Suit",
                   "Gravity Suit",
                   "X-Ray",
                   "Plasma",
                   "Grapple",
                   "Space Jump",
                   "Screw Attack",
                   "Morph Ball",
                   "Reserve Tank"]

    # create item array
    # 1 = spawn everything
    # 2 = spawn everything but reserve tanks
    # 3 = 2 and spawn everything but spazer, plasma and screw attack
    # 4 = 2 and spawn everything but ice
    # 5 = 3 and 4 combined
    CHARGE = 5
    ICE = 6
    HIJUMP = 7
    SPEED = 8
    WAVE = 9
    SPAZER = 10
    SPRING = 11
    VARIA = 12
    GRAVITY = 13
    XRAY = 14
    PLASMA = 15
    GRAPPLE = 16
    SPACE = 17
    SCREW = 18
    RESERVE = 20
    itemArray = [CHARGE,HIJUMP,SPEED,WAVE,SPRING,VARIA,GRAVITY,XRAY,GRAPPLE,SPACE]
    if itemFull == 1:
        itemArray = itemArray + [ICE,SPAZER,PLASMA,SCREW] + [RESERVE]*4
    if itemFull == 2:
        itemArray = itemArray + [ICE,SPAZER,PLASMA,SCREW]
    if itemFull == 3:
        itemArray = itemArray + [ICE]
    if itemFull == 4:
        itemArray = itemArray + [SPAZER,PLASMA,SCREW]
    etankArray = [ETANK]*itemCount[0]
    missileArray = [MISSILE]*(itemCount[1]-1)
    smissileArray = [SMISSILE]*itemCount[2]
    pbombArray = [PBOMB]*itemCount[3]
    itemArray = itemArray + etankArray
    itemArray = itemArray + missileArray
    itemArray = itemArray + smissileArray
    itemArray = itemArray + pbombArray

    while len(itemArray) < 100 - 3:
        pickup = random.randint(1,80)
        if pickup <= itemCount[0]:
            itemArray.append(ETANK)
        elif pickup <= itemCount[0] + itemCount[1]:
            itemArray.append(MISSILE)
        elif pickup <= itemCount[0] + itemCount[1] + itemCount[2]:
            itemArray.append(SMISSILE)
        else:
            itemArray.append(PBOMB)
    random.shuffle(itemArray)

    # set items
    # based off the code from Super Metroid Randomizer.
    offset1 = int("0x78000",0)
    offset1end = int("0x79192",0)
    offset2 = int("0x7c215",0)
    offset2end = int("0x7c7bb",0)
    currIndex = 0
    # items are of the form 0xeed7-0xefcf, and end in 3,7,11 or 15
    minType = int("0xeed7",0)
    maxType = int("0xefcf",0)
    chozoType = int("0xef2b",0)
    hiddenType = int("0xef7f",0)
    tempArray = [3,7,11,15]
    chozoMissile = int("0xef2f",0)
    morphBall = int("0xef23",0)
    bombs = int("0xef3b",0)
    defaultItems = [chozoMissile,morphBall,bombs]
    # debug data
    itemString = ""
    
    offsetArray = [ [offset1,offset1end],[offset2,offset2end] ]
    for i in offsetArray:
        offset = i[0]
        while offset < i[1]:
            halfword = hexMethods.getHalfword(fileName,hex(offset))
            itemType = int(halfword,0)
            if itemType % 16 in tempArray and itemType >= minType and itemType <= maxType and itemType not in defaultItems:
                
                # item found, determine type
                # normal type
                if itemType < chozoType:
                    itemString = stringArray[(itemType - minType)>>2]
                    # formula is minType + 16 every 4 items then + 3,7,11, or 15
                    item = minType-7 + (((itemArray[currIndex]+1)>>2)<<4) + tempArray[(itemArray[currIndex]+1) % 4]
                    
                # chozo type
                elif itemType < hiddenType:
                    itemString = "Chozo " + stringArray[(itemType - chozoType)>>2]
                    # same, but with minType
                    item = chozoType-11 + (((itemArray[currIndex]+2)>>2)<<4) + tempArray[(itemArray[currIndex]+2) % 4]
                    
                # hidden type
                else:
                    if itemType == maxType: itemString = "Hidden Reserve"
                    else: itemString = "Hidden " + stringArray[(itemType - hiddenType)>>2]
                    # for some reason reserve skips one?
                    if itemArray == RESERVE:
                        item = maxType
                    else:
                        item = hiddenType-15 + (((itemArray[currIndex]+3)>>2)<<4) + tempArray[(itemArray[currIndex]+3) % 4]
                        
                # write to ROM
                hexMethods.writeRawBytes(fileName,hex(offset),chr(item%256),1)
                hexMethods.writeRawBytes(fileName,hex(offset+1),chr(item/256),1)
                currIndex += 1
                print hex(offset),hex(item)

            offset += 2
    # debug
    # print currIndex, len(itemArray)

    # change pickup values
    # missiles
    # itemETank,itemMiss,itemSMiss,itemPBomb
    hexMethods.writeRawBytes(fileName,"0x260b8",chr(itemETank[0]),1)
    hexMethods.writeRawBytes(fileName,"0x26474",chr(itemETank[2]),1)
    hexMethods.writeRawBytes(fileName,"0x2693f",chr(itemETank[1]),1)
    
    hexMethods.writeRawBytes(fileName,"0x260dd",chr(itemMiss[0]),1)
    hexMethods.writeRawBytes(fileName,"0x264a6",chr(itemMiss[2]),1)
    hexMethods.writeRawBytes(fileName,"0x26977",chr(itemMiss[1]),1)

    hexMethods.writeRawBytes(fileName,"0x26102",chr(itemSMiss[0]),1)
    hexMethods.writeRawBytes(fileName,"0x264d8",chr(itemSMiss[2]),1)
    hexMethods.writeRawBytes(fileName,"0x269af",chr(itemSMiss[1]),1)

    hexMethods.writeRawBytes(fileName,"0x26127",chr(itemPBomb[0]),1)
    hexMethods.writeRawBytes(fileName,"0x2650a",chr(itemPBomb[2]),1)
    hexMethods.writeRawBytes(fileName,"0x269e7",chr(itemPBomb[1]),1)
    

# swaps doors at random.
def swapDoors(source,fileName,seed,easy=True,perc=100):
    # initialize seed
    random.seed(seed)
    # create seed
    seed = "v0.2_g"
    if easy:
        seed += "b"

    # create new file
    headerSize = detectHeader(source)
    data = open(source,"rb")
    dest = open(fileName,"wb")
    # the entire system assumes the ROM has 0x200 bytes of header (wups)
    if headerSize < int("0x200",0):
        for i in range(int("0x200",0) - headerSize):
            dest.write("\0")
        dest.write(data.read())
    else:
        dest.write(data.read()[headerSize-int("0x200",0):])
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

        seed += "_" + miscFunctions.pad(hex(len(shuffleArray))[2:],2) + "_"
        for i in shuffleArray:
            seed += miscFunctions.pad(hex(i)[2:],2)
    
        # filter a sublist
        downCount = len(downDoorArray)
        shuffleArray = permuteList(downCount)
        shuffleArray = shuffleArray[:(downCount*perc/100)]
        downDoorArray = percolate(downDoorArray,shuffleArray)
        upDoorArray = percolate(upDoorArray,shuffleArray)
        
        seed += "_" + miscFunctions.pad(hex(len(shuffleArray))[2:],2) + "_"
        for i in shuffleArray:
            seed += miscFunctions.pad(hex(i)[2:],2)
    else:
        seed += "_p"

    seed += "_"
    swapArray = swapDoorList(fileName,leftDoorArray,rightDoorArray,easy)
    for i in swapArray:
        seed += miscFunctions.pad(hex(i)[2:],2)
    swapArray = swapDoorList(fileName,upDoorArray,downDoorArray,easy)
    seed += "_"
    for i in swapArray:
        seed += miscFunctions.pad(hex(i)[2:],2)

    # remove the 0x200 header bytes.
    data = open(fileName,"rb")
    romData = data.read()[int("0x200",0):]
    data.close()
    dest = open(fileName,"wb")
    dest.write(romData)
    dest.close()

    return seed

# swaps doors at a local level
def swapDoorsLocal(source,fileName,seed,easy = True,perc=[100,100,100,100,100,100,100,100]):
    # initialize seed
    random.seed(seed)

    # create seed
    seed = "v0.2_l"
    if easy:
        seed += "b"

    # create new file
    headerSize = detectHeader(source)
    data = open(source,"rb")
    dest = open(fileName,"wb")
    # the entire system assumes the ROM has 0x200 bytes of header (wups)
    if headerSize < int("0x200",0):
        for i in range(int("0x200",0) - headerSize):
            dest.write("\0")
        dest.write(data.read())
    else:
        dest.write(data.read()[headerSize-int("0x200",0):])
    dest.close()
    data.close()

    locaArray1 = [["brinstar",0],
                  ["crateria",1],
                  ["maridia",2],
                  ["norfair",4],
                  ["wreck",3],]

    locaArray2 = [["itemsA",6],
                  ["itemsB",6],
                  ["lower",5],]
    
    folder = "local-data/doors-"

    # record which areas have percentage bytes
    percRecord = 0
    if perc[0] == 100:
        percRecord += 1
    percRecord = percRecord<<1
    if perc[1] == 100:
        percRecord += 1
    percRecord = percRecord<<1
    if perc[2] == 100:
        percRecord += 1
    percRecord = percRecord<<1
    if perc[4] == 100:
        percRecord += 1
    percRecord = percRecord<<1
    if perc[3] == 100:
        percRecord += 1
    percRecord = percRecord<<1
    # duplicate entries for item rooms.
    if perc[6] == 100:
        percRecord += 1
    percRecord = percRecord<<1
    if perc[6] == 100:
        percRecord += 1
    percRecord = percRecord<<1
    if perc[5] == 100:
        percRecord += 1
    seed += "_" + miscFunctions.pad(hex(percRecord)[2:],2)
    
    # read doors by location (up/down and left/right)
    for i in locaArray1:
        name = i[0]
        leftDoorArray = miscFunctions.importList(folder + name + "-left.txt",
                                                 [HEX_FILTER,HEX_FILTER])
        rightDoorArray = miscFunctions.importList(folder + name + "-right.txt",
                                                  [HEX_FILTER,HEX_FILTER])
        downDoorArray = miscFunctions.importList(folder + name + "-down.txt",
                                                 [HEX_FILTER,HEX_FILTER])
        upDoorArray = miscFunctions.importList(folder + name + "-up.txt",
                                               [HEX_FILTER,HEX_FILTER])

        if perc[i[1]] != 100:
            # filter a sublist
            leftCount = len(leftDoorArray)
            shuffleArray = permuteList(leftCount)
            shuffleArray = shuffleArray[:(leftCount*perc[i[1]]/100)]
            leftDoorArray = percolate(leftDoorArray,shuffleArray)
            rightDoorArray = percolate(rightDoorArray,shuffleArray)

            seed += "_" + miscFunctions.pad(hex(len(shuffleArray))[2:],2) + "_"
            for j in shuffleArray:
                seed += miscFunctions.pad(hex(j)[2:],2)

            # filter a sublist
            downCount = len(downDoorArray)
            shuffleArray = permuteList(downCount)
            shuffleArray = shuffleArray[:(downCount*perc[i[1]]/100)]
            downDoorArray = percolate(downDoorArray,shuffleArray)
            upDoorArray = percolate(upDoorArray,shuffleArray)

            seed += "_" + miscFunctions.pad(hex(len(shuffleArray))[2:],2) + "_"
            for j in shuffleArray:
                seed += miscFunctions.pad(hex(j)[2:],2)

        swapArray = swapDoorList(fileName,leftDoorArray,rightDoorArray,easy)
        seed += "_"
        for j in swapArray:
            seed += miscFunctions.pad(hex(j)[2:],2)
        swapArray = swapDoorList(fileName,upDoorArray,downDoorArray,easy)
        seed += "_"
        for j in swapArray:
            seed += miscFunctions.pad(hex(j)[2:],2)

    # read doors by location (left/right only)
    for i in locaArray2:
        name = i[0]
        leftDoorArray = miscFunctions.importList(folder + name + "-left.txt",
                                                 [HEX_FILTER,HEX_FILTER])
        rightDoorArray = miscFunctions.importList(folder + name + "-right.txt",
                                                  [HEX_FILTER,HEX_FILTER])

        if perc[i[1]] != 100:
            # filter a sublist
            leftCount = len(leftDoorArray)
            shuffleArray = permuteList(leftCount)
            shuffleArray = shuffleArray[:(leftCount*perc[i[1]]/100)]
            leftDoorArray = percolate(leftDoorArray,shuffleArray)
            rightDoorArray = percolate(rightDoorArray,shuffleArray)
            
            seed += "_" + miscFunctions.pad(hex(len(shuffleArray))[2:],2) + "_"
            for j in shuffleArray:
                seed += miscFunctions.pad(hex(j)[2:],2)

        # force item doors to be a backtracking shuffle.
        if name == "lower":
            swapArray = swapDoorList(fileName,leftDoorArray,rightDoorArray,easy)
        else:
            swapArray = swapDoorList(fileName,leftDoorArray,rightDoorArray,True)
        seed += "_"
        for j in swapArray:
            seed += miscFunctions.pad(hex(j)[2:],2)

    # remove the 0x200 header bytes.
    data = open(fileName,"rb")
    romData = data.read()[int("0x200",0):]
    data.close()
    dest = open(fileName,"wb")
    dest.write(romData)
    dest.close()
    
    return seed

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

    return swapArray

# swaps the contents of two door arrays with a provided swap array.
# arrays must have the same length.
def swapDoorListSeed(fileName,doorList1,doorList2,swapArray,easy = True):
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
    print "Welcome to the Super Metroid Super Randomizer."
    print "This application randomizes a variety of things in Super Metroid."
    print "For additional information, type h at any step of the process."
    print "--------------"

    currInput = ""
    print "Do you have a pre-generated seed? (Type 1 or 2.)"
    print "1. Yes"
    print "2. No"
    while(currInput != "1" and currInput != "2"):
        currInput = raw_input("-> ")
        if currInput == "h":
            print "A pre-generated seed is created by this application to duplicate a specific randomization."
            print "If you are creating a new randomization, you shouldn't have a pre-generated seed."

    if currInput == "1":
        currInput = ""
        while(currInput == ""):
            print "Type the filename of the clean rom to reference."
            print "(This file should be in the same folder as the executable.)"
            currInput = raw_input("-> ")
        source = currInput

        currInput = ""
        while(currInput == ""):
            print "Type the filename to output to."
            print "Warning: Use a different filename from the original ROM."
            currInput = raw_input("-> ")
        output = currInput

        seed = "v0.2"
        while not seedChecksum(seed)[0]:
            print "Type the filename of text file with your seed value."
            print "(This file should be in the same folder as the executable.)"
            currInput = raw_input("-> ")
            data = open(currInput,"r")
            seed = data.readline()
            data.close()
            if not seedChecksum(seed)[0]:
                print "Your seed is invalid..."

        print "processing ROM..."
        swapDoorsSeed(source,output,seed)
        print "Done! For reference, the ROM header has been normalized to 0"
        print "if you want to combine this utility with something else."
        print "Reminder: The morph ball, the missiles nearby"
        print "and the bombs are always fixed."
        print "So is Ceres Station and Tourian."

        os.system("pause")
        return 0
            

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

    if globalType:
        # get the percentage for global shuffling
        currInput = ""
        while 1:
            print "Pick your randomization level. (Pick a value between 10-100)"
            currInput = raw_input("-> ")
            if currInput == "h":
                print "The randomization level will determine how many doors"
                print "are shuffled. Higher percentages mean more doors."
            else:
                try:
                    percentage = int(currInput)
                except ValueError:
                    print "This value isn't a number."
                    continue
                else:
                    if not (percentage <= 100 and percentage >= 10):
                        print "This value isn't between 10 and 100."
                        continue
                    else:
                        break
    else:
        # get the percentage for local shuffling
        currInput = 0
        print "For local randomization, you can choose"
        print "the randomization percentage of each area."
        print "Note that item rooms are considered a separate area."
        print "If you set a nonzero percentage for item rooms,"
        print "you can still be sent between areas through them."
        print "Note that there are default values,"
        print "which set randomization to 100% for all areas"
        print "except item rooms."
        while(currInput != "1" and currInput != "2"):
            print "Select if you want to use the default values (100% to all areas) (Type 1 or 2.)"
            print "1. Default Values"
            print "2. Custom Values"
            currInput = raw_input("-> ")
            if currInput == "h":
                print "The default values set each area to 100%."
                print "Custom values will ask you to set the percentages for each area."
        if currInput == "1":
            percentage = [100,100,100,100,100,100,100]
        else:
            locaArray = ["Brinstar",
                         "Crateria",
                         "Maridia",
                         "the Wrecked Ship",
                         "Norfair",
                         "Lower Norfair",
                         "Item Rooms",]
            percentage = []
            for i in locaArray:
                while 1:
                    print "Pick your randomization level for " + i + ". (Pick a value between 0-100)"
                    currInput = raw_input("-> ")
                    if currInput == "h":
                        print "The randomization level will determine how many doors"
                        print "are shuffled. Higher percentages mean more doors."
                    else:
                        try:
                            tempPerc = int(currInput)
                        except ValueError:
                            print "This value isn't a number."
                            continue
                        else:
                            if not (tempPerc <= 100 and tempPerc >= 0):
                                print "This value isn't between 0 and 100."
                                continue
                            else:
                                percentage.append(tempPerc)
                                break

    currInput = ""
    while(currInput == ""):
        print "Type a seed. (This can be anything.)"
        currInput = raw_input("-> ")
    seed = currInput

    itemRandom = False
    itemFull = 1
    itemETank = [100,100,100]
    itemMiss = [5,5,5]
    itemSMiss = [5,5,5]
    itemPBomb = [5,5,5]
    itemCount = [14,46,10,10]
    currInput = ""
    print "Do you want to randomize items?"
    print "1. Yes"
    print "2. No"
    while(currInput != "1" and currInput != "2"):
        currInput = raw_input("-> ")
        if currInput == "h":
            print "This will shuffle the items. There are several options available:"
            print "You can select whether unique items can replace common items."
            print "You can also change the amount of a common item you receive during a pickup."
            print "This value can be changed based on whether the item is hidden,"
            print "found in the open, or found on a Chozo statue."
    if currInput == "1":
        itemRandom = True

        # randomize items
        # randomization type
        #currInput = ""
        #while(currInput not in ["1","2"]):
        #    print "First, do you want to have unique items mix with common items?"
        #    print "1. Yes"
        #    print "2. No"
        #    currInput = raw_input("-> ")
        #    if currInput == "h":
        #        print "This determines if unique items can spawn outside of Chozo statues."
        #if currInput == "1":
        #    itemFull = True

        # item count
        currInput = ""
        while(currInput not in ["1","2","3","4","5"]):
            print "Pick the ratio of items to spawn."
            print "The values are, in order:"
            print "E-tanks, Missiles, Super Missiles, Power Bombs"
            print "1. 14 / 46 / 10 / 10 (default)"
            print "2. 20 / 20 / 20 / 20 (balanced)"
            print "3. 50 / 10 / 10 / 10 (Health)"
            print "4. 10 / 10 / 50 / 10 (Super Missiles)"
            print "5. 10 / 10 / 10 / 50 (Power Bombs)"
            currInput = raw_input("-> ")
            if currInput == "h":
                print "This determines the amount of each type of item to spawn."
        if currInput == "1":
            itemCount = [14,46,10,10]
        if currInput == "2":
            itemCount = [20,20,20,20]
        if currInput == "3":
            itemCount = [50,10,10,10]
        if currInput == "4":
            itemCount = [10,10,50,10]
        if currInput == "5":
            itemCount = [10,10,10,50]

        # unique item difficulties
        currInput = ""
        while(currInput not in ["1","2","3","4","5"]):
            print "Pick the rarity of unique items."
            print "1. Normal difficulty (Spawns all unique items.)"
            print "2. Medium difficulty (Does not spawn reserve tanks.)"
            print "3. Hard difficulty (In addition to medium difficulty, does not spawn Spazer Beam, Plasma Beam or Screw Attack.)"
            print "4. Very Hard difficulty (In addition to medium difficulty, does not spawn Ice Beam.)"
            print "5. Insane difficulty (Combines Hard and Very Hard.)"
            currInput = raw_input("-> ")
            if currInput == "h":
                print "This determines how many unique items to seed in the game."
        if currInput == "1":
            itemFull = 1
        if currInput == "2":
            itemFull = 2
        if currInput == "3":
            itemFull = 3
        if currInput == "4":
            itemFull = 4
        if currInput == "5":
            itemFull = 5

        # E-Tank values
        currInput = ""
        while(currInput not in ["1","2","3","4"]):
            print "Which spread do you want for E-Tanks? This is the amount of health per pickup."
            print "The values are E-tanks found in the open, Hidden E-tanks and Chozo E-tanks."
            print "1. 100 / 100 / 100 (default)"
            print "2. 100 / 50 / 100 (medium)"
            print "3. 50 / 10 / 200 (hard)"
            print "4. 50 / 50 / 50 (very hard)"
            currInput = raw_input("-> ")
            if currInput == "h":
                print "This determines the amount of health obtained per E-tank pickup."
        if currInput == "1":
            itemETank = [100,100,100]
        if currInput == "2":
            itemETank = [100,50,100]
        if currInput == "3":
            itemETank = [50,10,200]
        if currInput == "4":
            itemETank = [50,50,50]

        # Missile values
        currInput = ""
        while(currInput not in ["1","2","3","4"]):
            print "Which spread do you want for Missiles? This is the amount of missiles per pickup."
            print "Note that Chozo Missiles are a minimum of 5 in order to open red doors."
            print "The values are Missiles found in the open, Hidden Missiles and Chozo Missiles."
            print "1. 5 / 5 / 5 (default)"
            print "2. 5 / 2 / 10 (medium)"
            print "3. 5 / 1 / 5 (hard)"
            print "4. 1 / 1 / 5 (very hard)"
            currInput = raw_input("-> ")
            if currInput == "h":
                print "This determines the amount of missiles obtained per pickup."
        if currInput == "1":
            itemMiss = [5,5,5]
        if currInput == "2":
            itemMiss = [5,2,10]
        if currInput == "3":
            itemMiss = [5,1,5]
        if currInput == "4":
            itemMiss = [1,1,5]

        # Super Missile values
        currInput = ""
        while(currInput not in ["1","2","3","4"]):
            print "Which spread do you want for Super Missiles?"
            print "This is the amount of super missiles per pickup."
            print "The values are Super Missiles found in the open,"
            print "Hidden Super Missiles and Chozo Super Missiles."
            print "1. 5 / 5 / 5 (default)"
            print "2. 2 / 2 / 10 (medium)"
            print "3. 1 / 1 / 5 (hard)"
            print "4. 1 / 1 / 2 (very hard)"
            currInput = raw_input("-> ")
            if currInput == "h":
                print "This determines the amount of Super Missiles obtained per pickup."
        if currInput == "1":
            itemSMiss = [5,5,5]
        if currInput == "2":
            itemSMiss = [2,2,10]
        if currInput == "3":
            itemSMiss = [1,1,5]
        if currInput == "4":
            itemSMiss = [1,1,2]

        # Power Bomb values
        currInput = ""
        while(currInput not in ["1","2","3","4"]):
            print "Which spread do you want for Power Bombs?"
            print "This is the amount of power bombs per pickup."
            print "The values are Power Bombs found in the open,"
            print "Hidden Power Bombs and Chozo Power Bombs."
            print "1. 5 / 5 / 5 (default)"
            print "2. 2 / 2 / 5 (medium)"
            print "3. 1 / 1 / 2 (hard)"
            print "4. 1 / 1 / 1 (very hard)"
            currInput = raw_input("-> ")
            if currInput == "h":
                print "This determines the amount of Power Bombs obtained per pickup."
        if currInput == "1":
            itemPBomb = [5,5,5]
        if currInput == "2":
            itemPBomb = [2,2,5]
        if currInput == "3":
            itemPBomb = [1,1,2]
        if currInput == "4":
            itemPBomb = [1,1,1]

        # item seed
        currInput = ""
        while(currInput == ""):
            print "Type a second seed. (This can be anything.)"
            currInput = raw_input("-> ")
        seed2 = currInput

    currInput = ""
    while(currInput == ""):
        print "Type the filename of the clean rom to reference."
        print "(This file should be in the same folder as the executable.)"
        currInput = raw_input("-> ")
    source = currInput

    currInput = ""
    while(currInput == ""):
        print "Type the filename to output to."
        print "Warning: Use a different filename from the original ROM."
        currInput = raw_input("-> ")
    output = currInput
            
    print "processing ROM..."
    if globalType:
        seed = swapDoors(source,output,seed,easyMode,percentage)
    else:
        seed = swapDoorsLocal(source,output,seed,easyMode,percentage)
    if itemRandom:
        swapItems(output,seed2,itemRandom,itemFull,itemETank,itemMiss,itemSMiss,itemPBomb,itemCount)
        
    print "Done! For reference, the ROM header has been normalized to 0"
    print "if you want to combine this utility with something else."
    print "Reminder: The morph ball, the missiles nearby"
    print "and the bombs are always fixed."
    print "So is Ceres Station and Tourian."

    print "\nYour seed is:"
    print seed
    print "\nThis value has been saved in seed.txt."
    data = open("seed.txt","w")
    data.write(seed)
    data.close()
    
    os.system("pause")

# tests seeder
def seedTest(testCount1,testCount2):
    # test 10 global checks
    for i in range(testCount1):
        if random.randint(0,1):
            perc = random.randint(1,99)
        else:
            perc = 100
        backtrack = random.randint(0,1)
        seed = swapDoors("clean-rom.smc","test_gCont_" + str(i) + ".smc",random.random(),easy=backtrack,perc=perc)
        swapDoorsSeed("clean-rom.smc","test_gSeed_" + str(i) + ".smc",seed)
    for i in range(testCount2):
        j = random.randint(0,127)
        flag = 1
        perc = []
        backtrack = random.randint(0,1)
        for k in range(7):
            if flag&j != 0:
                perc.append(100)
            else:
                perc.append(random.randint(0,99))
            flag = flag << 1
        seed = swapDoorsLocal("clean-rom.smc","test_lCont_" + str(i) + ".smc",random.random(),easy=backtrack,perc=perc)
        swapDoorsSeed("clean-rom.smc","test_lSeed_" + str(i) + ".smc",seed)

# test checksums
def seedChecksumTest(testCount1,testCount2):
    # test 10 global checks
    for i in range(testCount1):
        if random.randint(0,1):
            perc = random.randint(1,99)
        else:
            perc = 100
        backtrack = random.randint(0,1)
        seed = swapDoors("clean-rom.smc","test.smc",random.random(),easy=backtrack,perc=perc)
        print seedChecksum(seed)
    for i in range(testCount2):
        j = random.randint(0,127)
        flag = 1
        perc = []
        backtrack = random.randint(0,1)
        for k in range(7):
            if flag&j != 0:
                perc.append(100)
            else:
                perc.append(random.randint(0,99))
            flag = flag << 1
        seed = swapDoorsLocal("clean-rom.smc","test.smc",random.random(),easy=backtrack,perc=perc)
        print seedChecksum(seed)

if __name__ == "__main__":
    main()
    #itemRandom = False
    #itemFull = 1
    #itemETank = [100,100,100]
    #itemMiss = [5,5,5]
    #itemSMiss = [5,5,5]
    #itemPBomb = [5,5,5]
    #itemCount = [14,46,10,10]
    #swapItems("test.smc",0,itemRandom,itemFull,itemETank,itemMiss,itemSMiss,itemPBomb,itemCount)
