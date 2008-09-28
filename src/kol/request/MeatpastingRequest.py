from kol.Error import InvalidRecipeError, NotEnoughItemsError, NotEnoughAdventuresLeftError, RequestError
from kol.database import ItemDatabase
from kol.manager import PatternManager
from kol.request.GenericRequest import GenericRequest

class MeatpastingRequest(GenericRequest):

	def __init__(self, session, itemid1, itemid2, numPasted=1, makeMax=False):
		super(MeatpastingRequest, self).__init__(session)
		self.url = session.serverURL + "craft.php"
		self.requestData['mode'] = 'combine'
		self.requestData['pwd'] = session.pwd
		self.requestData['action'] = 'craft'
		self.requestData['qty'] = numPasted
		self.requestData['a'] = itemid1
		self.requestData['b'] = itemid2
		
		if makeMax:
			self.requestData['max'] = "on"
	
	def parseResponse(self):
		dontHaveMeatpastePattern = PatternManager.getOrCompilePattern('noMeatpaste')
		itemsDontMeatpastePattern = PatternManager.getOrCompilePattern('itemsDontMeatpaste')
		dontHaveItemsPattern = PatternManager.getOrCompilePattern('dontHaveItemsMeatpaste')
		
		# Check for errors.
		if dontHaveMeatpastePattern.search(self.responseText):
			raise NotEnoughItemsError("Unable to combine items. You don't have any meatpaste.")
		elif itemsDontMeatpastePattern.search(self.responseText):
			raise InvalidRecipeError("Unable to combine items. The submitted ingredients do not meatpaste together.")
		elif dontHaveItemsPattern.search(self.responseText):
			raise NotEnoughItemsError("Unable to combine items. You don't have all of the items you are trying to meatpaste.")
			
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
