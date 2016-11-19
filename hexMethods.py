# Version 13.08.30
import struct
from struct import *

def getWord(source,offset):
    # this routine gets the word written at the given offset (returns the hex value)
    data = open(source, "rb")
    currLoc = int(offset,0)
    data.seek(currLoc)
    currRead = data.read(4)
    data.close()
    array = unpack("BBBB",currRead)
    return arrayToByte(array)

def getHalfword(source,offset):
    # this routine gets the word written at the given offset (returns the hex value)
    data = open(source, "rb")
    currLoc = int(offset,0)
    data.seek(currLoc)
    currRead = data.read(2)
    data.close()
    array = unpack("BB",currRead)
    return arrayToByte(array)

def getByte(source,offset):
    # this routine gets the byte written at the given offset (returns the hex value)
    data = open(source, "rb")
    currLoc = int(offset,0)
    data.seek(currLoc)
    currRead = data.read(1)
    data.close()
    array = unpack("B",currRead)
    return arrayToByte(array)

def getRawByte(source,offset):
    # this routine gets the byte written at the given offset (returns the hex value)
    data = open(source, "rb")
    currLoc = int(offset,0)
    data.seek(currLoc)
    return data.read(1)

def getRawBytes(source,offset,length):
    # this routine gets the byte written at the given offset (returns the hex value)
    data = open(source, "rb")
    currLoc = int(offset,0)
    data.seek(currLoc)
    result = data.read(length)
    data.close()
    return result

def writeRawBytes(source,offset,byte,length):
    # this routine writes the given byte at the given offset
    data = open(source, "r+b")
    currLoc = int(offset,0)
    data.seek(currLoc)
    data.write(byte)
    data.close()

def arrayToByte(array):
    # converts an array of integers into bytes
    word = ""
    for i in range(0,len(array)):
        currentByte = hex(array[i])[2:]
        if len(currentByte) < 2:
            currentByte = "0" + currentByte
        word = currentByte + word
    return "0x" + word
