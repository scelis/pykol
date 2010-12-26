def getInteger(obj, key, defaultValue):
    ret = defaultValue
    if key in obj:
        try:
            ret = int(obj[key])
        except ValueError:
            pass
    return ret

def getString(obj, key, defaultValue):
    ret = defaultValue
    if key in obj:
        ret = obj[key]
    return ret

def getBoolean(obj, key, defaultValue):
    ret = defaultValue
    if key in obj:
        val = obj[key]
        if type(val) == str and len(val) > 0:
            if val[0] in ['T', 't', '1', 'y', 'Y']:
                ret = True
            elif val[0] in ['F', 'f', '0', 'n', 'N']:
                ret = False
        elif type(val) == int:
            if ret == 0:
                ret = False
            else:
                ret = True
        elif type(val) == bool:
            ret = val
    return ret
