__config = {}

def get(key, default=None):
    if key in __config:
        return __config[key]
    return default

def set(key, value, override=True):
    if override == True or key not in __config:
        __config[key] = value

def remove(key):
    if key in __config:
        del __config[key]
