from GenericRequest import GenericRequest
from kol.Error import InvalidRecipeError, NotEnoughItemsError, NotEnoughAdventuresLeftError, RequestError
from kol.manager import PatternManager
from kol.util import ParseResponseUtils

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
		# Check for errors.
		dontHaveMeatpastePattern = PatternManager.getOrCompilePattern('noMeatpaste')
		itemsDontMeatpastePattern = PatternManager.getOrCompilePattern('itemsDontMeatpaste')
		dontHaveItemsPattern = PatternManager.getOrCompilePattern('dontHaveItemsMeatpaste')
		if dontHaveMeatpastePattern.search(self.responseText):
			raise NotEnoughItemsError("Unable to combine items. You don't have any meatpaste.")
		elif itemsDontMeatpastePattern.search(self.responseText):
			raise InvalidRecipeError("Unable to combine items. The submitted ingredients do not meatpaste together.")
		elif dontHaveItemsPattern.search(self.responseText):
			raise NotEnoughItemsError("Unable to combine items. You don't have all of the items you are trying to meatpaste.")
			
		# Find the items attached to the message.
		items = ParseResponseUtils.parseItemsReceived(self.responseText)
		if len(items) > 0:
			self.responseData["items"] = item
		else:
			raise RequestError("Unknown error.")
