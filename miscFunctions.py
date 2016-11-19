# Import list takes two inputs, a file source, and a filter list.
# It will return an array. Each array entry will be an array,
# and the entries will be the strings of each line
# separated by whitespace, with charactered filtered by filter type.
# filters are a string of acceptable characters.
# note that the program will halt if it detects that a line does not
# have enough entries corresponding to filters
def importList(fileSource,filterTypes):
    data = open(fileSource,"r")
    fileArray = data.readlines()
    resultArray = []
    entryNum = len(filterTypes)

    for i in fileArray:
        i = i.strip("\n")
        entries = i.split()
        assert len(entries) >= entryNum, "WARNING: Not enough columns - " + i
        if entryNum > 1:
            resultEntry = []
            for j in range(0,entryNum):
                resultEntry.append(''.join(char for char in entries[j]
                                           if char in filterTypes[j]))
        else:
            resultEntry = ''.join(char for char in entries[0]
                                  if char in filterTypes[0])

        resultArray.append(resultEntry)

    return resultArray

# returns the signed integer (between -128,127)
# corresponding to the given integer.
def signedByte(byteData):
    if byteData > int("0x7f",0):
        return byteData - 256
    else:
        return byteData

# pads a string until it is X characters long.
def tab(string,length):
    while len(string) < length:
        string = string + " "
    return string

# returns a string of a fixed length that corresponds to the given integer.
# The given integer must be shorter than the pad length.
def pad(integer,length):
    string = str(integer)
    while len(string) < length:
        string = "0" + string
    return string
