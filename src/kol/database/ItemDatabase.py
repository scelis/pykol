"This module is used as a database for KoL item information."

from kol.Error import ItemNotFoundError
from kol.data import Items
from kol.manager import FilterManager
from kol.util import Report

__isInitialized = False
__itemsById = {}
__itemsByDescId = {}
__itemsByName = {}

def init():
    """
    Initializes the ItemDatabase. This method should be called before the 
    database is ever accessed as it ensures that the database is populated
    with all of the data it needs.
    """
    global __isInitialized
    if __isInitialized == True:
        return
    
    Report.trace("itemdatabase", "Initializing the item database.")
    returnCode = FilterManager.executeFiltersForEvent("preInitializeItemDatabase")
    if returnCode == FilterManager.FINISHED:
        Report.trace("itemdatabase", "Item database initialized.")
        __isInitialized = True
        return
        
    for item in Items.items:
        addItem(item)
    
    FilterManager.executeFiltersForEvent("postInitializeItemDatabase")
    __isInitialized = True
    Report.trace("itemdatabase", "Item database initialized.")

def addItem(item):
    "Adds an item to the database."
    if "plural" not in item:
        item["plural"] = item["name"] + "s"
    __itemsById[item["id"]] = item
    __itemsByDescId[item["descId"]] = item
    __itemsByName[item["name"]] = item

def getItemFromId(itemId, session=None):
    "Returns information about an item given its ID."
    if not __isInitialized:
        init()
    
    try:
        return __itemsById[itemId].copy()
    except KeyError:
        cxt = {}
        FilterManager.executeFiltersForEvent("couldNotFindItem", cxt, session=session, itemId=itemId)
        if "item" in cxt:
            item = cxt["item"]
            addItem(item)
            return item.copy()
        raise ItemNotFoundError("Item ID %s is unknown." % itemId)

def getItemFromDescId(descId, session=None):
    "Returns information about an item given its description ID."
    if not __isInitialized:
        init()
    
    try:
        return __itemsByDescId[descId].copy()
    except KeyError:
        cxt = {}
        FilterManager.executeFiltersForEvent("couldNotFindItem", cxt, session=session, descId=descId)
        if "item" in cxt:
            item = cxt["item"]
            addItem(item)
            return item.copy()
        raise ItemNotFoundError("Item with description ID %s is unknown." % descId)

def getItemFromName(itemName, session=None):
    "Returns information about an item given its name."
    if not __isInitialized:
        init()
    
    try:
        return __itemsByName[itemName].copy()
    except KeyError:
        cxt = {}
        FilterManager.executeFiltersForEvent("couldNotFindItem", cxt, session=session, itemName=itemName)
        if "item" in cxt:
            item = cxt["item"]
            addItem(item)
            return item.copy()
        raise ItemNotFoundError("The item '%s' is unknown." % itemName)
