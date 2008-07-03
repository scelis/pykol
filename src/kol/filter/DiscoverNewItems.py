from kol.manager import FilterManager
from kol.request.ClosetContentsRequest import ClosetContentsRequest
from kol.request.ItemDescriptionRequest import ItemDescriptionRequest
from kol.util import Report

def doFilter(eventName, context, **kwargs):
	if eventName == "couldNotFindItem":
		couldNotFindItem(context, **kwargs)

def couldNotFindItem(context, **kwargs):
	session = None
	item = None
	
	if "session" in kwargs:
		session = kwargs["session"]
		
		if "descId" in kwargs:
			r = ClosetContentsRequest(session)
			r.doRequest()
			item = r.getItemInformationFromDescId(kwargs["descId"])
		if "itemId" in kwargs:
			r = ClosetContentsRequest(session)
			r.doRequest()
			item = r.getItemInformationFromItemId(kwargs["itemId"])
		if "itemName" in kwargs:
			r = ClosetContentsRequest(session)
			r.doRequest()
			item = r.getItemInformationFromItemName(kwargs["itemName"])
	
	if item != None:
		r = ItemDescriptionRequest(session, item["descId"])
		r.doRequest()
		r.addInformationToItem(item)
		
		Report.trace("itemdatabase", "Discovered new item:" + str(item))
		
		context["item"] = item
		FilterManager.executeFiltersForEvent("discoveredNewItem", session=session, item=item)
