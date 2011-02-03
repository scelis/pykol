"""
This module allows scripts and bots to use a tab-delimited file as a place to
store and retrieve item information instead of using the standard
ItemDatabase. This is useful when scripts only need to know basic information
about each item.
"""

from kol.database import ItemDatabase
from kol.manager import FilterManager

_path = None

def doFilter(eventName, context, **kwargs):
    returnCode = FilterManager.CONTINUE

    if eventName == "preInitializeItemDatabase":
        returnCode = preInitializeItemDatabase(context, **kwargs)
    elif eventName == "discoveredNewItem":
        returnCode = discoveredNewItem(context, **kwargs)

def preInitializeItemDatabase(context, **kwargs):
    f = None
    try:
        f = open(_path, "r")
    except IOError:
        pass

    if f != None:
        line = f.readline()
        while len(line) > 0:
            line = line.strip(" \r\n")
            if len(line) > 0 and line[0] != '#':
                arr = line.split('\t')
                itemId = int(arr[0])
                descId = int(arr[1])
                name = arr[2]
                image = arr[3]
                autosell = int(arr[4])
                item = {"id":itemId, "descId":descId, "name":name, "autosell":autosell, "image":image}
                ItemDatabase.addItem(item)
            line = f.readline()
        f.close()

    return FilterManager.FINISHED

def discoveredNewItem(context, **kwargs):
    if "item" in kwargs:
        item = kwargs["item"]
        f = open(_path, "a")
        f.write("%s\t%s\t%s\t%s\t%s\n" % (item["id"], item["descId"], item["name"], item["image"], item["autosell"]))
        f.close()

    return FilterManager.CONTINUE
