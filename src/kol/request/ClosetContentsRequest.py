from kol.Error import ItemNotFoundError
from GenericRequest import GenericRequest

import re

class ClosetContentsRequest(GenericRequest):
	def __init__(self, session):
		super(ClosetContentsRequest, self).__init__(session)
		self.url = session.serverURL + "closet.php"

	def getItemInformationFromDescId(self, descId):
		pattern = re.compile("<option value='([0-9]+)' descid='%s'>([^<>]*) \([0-9]+\)<\/option>" % descId)
		match = pattern.search(self.responseText)
		if match:
			item = {"id":int(match.group(1)), "descId":descId, "name":match.group(2)}
			return item
		else:
			raise ItemNotFoundError("Could not find item associated with description ID '%s'." % descId)
	
	def getItemInformationFromItemId(self, itemId):
		pattern = re.compile("<option value='%s' descid='([0-9]+)'>([^<>]*) \([0-9]+\)<\/option>" % itemId)
		match = pattern.search(self.responseText)
		if match:
			item = {"id":itemId, "descId":int(match.group(1)), "name":match.group(2)}
			return item
		else:
			raise ItemNotFoundError("Could not find item associated with ID '%s'." % itemId)
	
	def getItemInformationFromItemName(self, itemName):
		pattern = re.compile("<option value='([0-9]+)' descid='([0-9]+)'>%s \([0-9]+\)<\/option>" % itemName)
		match = pattern.search(self.responseText)
		if match:
			item = {"id":int(match.group(1)), "descId":int(match.group(2)), "name":itemName}
			return item
		else:
			raise ItemNotFoundError("Could not find item with name '%s'." % itemName)
