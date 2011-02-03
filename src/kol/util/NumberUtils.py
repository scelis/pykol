import locale

locale.setlocale(locale.LC_ALL, '')

def formatNumberWithCommas(number):
    return locale.format("%d", number, 1)

def parseIntegerFromHumanReadableString(intStr):
    # See if this is string ends in a 'k' or 'm'.
    isThousand = False
    isMillion = False
    if intStr[-1].lower() == 'm':
        isMillion = True
        intStr = intStr[:-1]
    elif intStr[-1].lower() == 'k':
        isThousand = True
        intStr = intStr[:-1]

    # Break the string up into parts.
    dotIndex = intStr.find('.')
    if dotIndex >= 0:
        integerPart = intStr[:dotIndex]
        decimalPart = intStr[dotIndex+1:]
    else:
        integerPart = intStr
        decimalPart = None

    # See if we can remove commas.
    commaIndex = integerPart.find(',')
    if commaIndex > 0:
        array = integerPart.split(',')
        isCommaStr = True
        i = 0
        while i < len(array) and isCommaStr:
            length = len(array[i])
            if i == 0:
                if length == 0 or length > 3:
                    isCommaStr = False
            else:
                if length != 3:
                    isCommaStr = False
            i += 1
        if isCommaStr:
            integerPart = integerPart.replace(",", "")

    # Determine the number.
    if decimalPart != None:
        num = float(integerPart + '.' + decimalPart)
    else:
        num = int(integerPart)
    if isMillion:
        num *= 1000000
    elif isThousand:
        num *= 1000
    return int(round(num))

def getDurationFromString(durationStr):
    duration = 0
    i = 0
    tmpNum = ""
    hasDays = False
    hasHours = False
    hasMinutes = False

    while i < len(durationStr):
        if durationStr[i].isdigit():
            tmpNum += str(durationStr[i])
        else:
            if len(tmpNum) == 0:
                raise ValueError("Invalid duration specified.")
            if durationStr[i] == 'd' and hasDays == False:
                duration += int(tmpNum) * 24 * 60
                hasDays = True
            elif durationStr[i] == 'h' and hasHours == False:
                duration += int(tmpNum) * 60
                hasHours = True
            elif durationStr[i] == 'm' and hasMinutes == False:
                duration += int(tmpNum)
                hasMinutes = True
            else:
                raise ValueError("Invalid duration specified.")
            tmpNum = ""
        i += 1

    if len(tmpNum) > 0:
        if duration == 0:
            duration = int(tmpNum) * 60
        else:
            raise ValueError("Invalid duration specified.")

    return duration
