"""
This module is used to discover information about items that don't already exist in the
ItemDatabase.
"""

from kol.Error import ItemNotFoundError
from kol.manager import FilterManager
from kol.request.ClosetContentsRequest import ClosetContentsRequest
from kol.request.ItemDescriptionRequest import ItemDescriptionRequest
from kol.util import Report

import re

def doFilter(eventName, context, **kwargs):
    returnCode = FilterManager.CONTINUE
    if eventName == "couldNotFindItem":
        returnCode = couldNotFindItem(context, **kwargs)
    return returnCode

def couldNotFindItem(context, **kwargs):
    if "session" not in kwargs:
        return FilterManager.CONTINUE

    session = kwargs["session"]
    item = None

    r = ClosetContentsRequest(session)
    r.skipParseResponse = True
    r.doRequest()

    if "descId" in kwargs:
        descId = kwargs["descId"]
        pattern = re.compile("<option value='([0-9]+)' descid='%s'>(.*?) \([0-9]+\)<\/option>" % descId)
        match = pattern.search(r.responseText)
        if match:
            item = {"id":int(match.group(1)), "descId":descId, "name":match.group(2)}
        else:
            raise ItemNotFoundError("Could not find item associated with description ID '%s'." % descId)

    elif "itemId" in kwargs:
        itemId = kwargs["itemId"]
        pattern = re.compile("<option value='%s' descid='([0-9]+)'>(.*?) \([0-9]+\)<\/option>" % itemId)
        match = pattern.search(r.responseText)
        if match:
            item = {"id":itemId, "descId":int(match.group(1)), "name":match.group(2)}
        else:
            raise ItemNotFoundError("Could not find item associated with ID '%s'." % itemId)

    elif "itemName" in kwargs:
        itemName = kwargs["itemName"]
        pattern = re.compile("<option value='([0-9]+)' descid='([0-9]+)'>%s \([0-9]+\)<\/option>" % itemName)
        match = pattern.search(r.responseText)
        if match:
            item = {"id":int(match.group(1)), "descId":int(match.group(2)), "name":itemName}
        else:
            raise ItemNotFoundError("Could not find item with name '%s'." % itemName)

    if item != None:
        r = ItemDescriptionRequest(session, item["descId"])
        itemInfo = r.doRequest()
        for k,v in itemInfo.iteritems():
            item[k] = v

        Report.trace("itemdatabase", "Discovered new item: %s" % item)

        context["item"] = item
        FilterManager.executeFiltersForEvent("discoveredNewItem", context, session=session, item=item)
