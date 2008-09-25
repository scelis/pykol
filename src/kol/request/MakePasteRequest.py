from kol.Error import NotEnoughMeatError, RequestError
from kol.database import ItemDatabase
from kol.manager import PatternManager
from kol.request.GenericRequest import GenericRequest

"""
This request is used to combine meat into various other things.
the 'whichItem' parameter corresponds to the following things:
	1 = meat paste
	2 = meat stack
	3 = dense meat stack
"""

class MakePasteRequest(GenericRequest):

	def __init__(self, session, whichItem, quantity=1):
		super(MakePasteRequest, self).__init__(session)
		self.url = session.serverURL + "craft.php"
		self.requestData['pwd'] = session.pwd
		self.requestData['action'] = 'makepaste'
		self.requestData['qty'] = quantity
		
		if whichItem == 1:
			self.requestData['whichitem'] = 25
		elif whichItem == 2:
			self.requestData['whichitem'] = 88
		elif whichItem == 3:
			self.requestData['whichitem'] = 258
		else:
			raise RequestError("Invalid item passed to MakePasteRequest")
		
	def parseResponse(self):
		noMeatForPastePattern = PatternManager.getOrCompilePattern('noMeatForMeatpasting')
		
		# Check for errors.
		if noMeatForPastePattern.search(self.responseText):
			raise NotEnoughMeatError("Unable to make the requested item. You don't have enough meat")

		# Find the items attached to the message.
		singleItemPattern = PatternManager.getOrCompilePattern('acquireSingleItem')
		match = singleItemPattern.search(self.responseText)
		if match:
			descId = int(match.group(1))
			item = ItemDatabase.getItemFromDescId(descId, self.session)
			item["quantity"] = 1
		else:
			multiItemPattern = PatternManager.getOrCompilePattern('acquireMultipleItems')
			match = multiItemPattern.search(self.responseText)
			if match:
				descId = int(match.group(1))
				item = ItemDatabase.getItemFromDescId(descId, self.session)
				quantity = int(match.group(2).replace(',', ''))
				item["quantity"] = quantity
			else:
				raise RequestError("Unknown error.")
		
		self.responseData["items"] = item
