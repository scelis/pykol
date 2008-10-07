from GenericRequest import GenericRequest
from kol.Error import RequestError
from kol.manager import PatternManager
from kol.util import ParseResponseUtils

class MallItemPurchaseRequest(GenericRequest):
	"""
	Purchases an item from the specified store. This will fail if the price per item is not given
	correctly or if the quantity is higher than the remaining quantity per day. It will purchase
	as many as possible if the quantity is higher than the number in the store.
	"""

	def __init__(self, session, storeId, itemId, price, quantity=1):
		super(MallItemPurchaseRequest, self).__init__(session)
		self.url = session.serverURL + 'mallstore.php'
		self.requestData['pwd'] = session.pwd
		self.requestData['whichstore'] = storeId
		self.requestData['buying'] = "Yep."
		self.requestData['whichitem'] = str(itemId) + str(price).zfill(9)
		self.requestData['quantity'] = quantity

	def parseResponse(self):
		items = ParseResponseUtils.parseItemsReceived(self.responseText, self.session)
		if len(items) == 0:
			raise RequestError("Unknown error.")
		self.responseData["items"] = items
		
		spentMeatPattern = PatternManager.getOrCompilePattern('meatSpent')
		match = spentMeatPattern.search(self.responseText)
		self.responseData['meatSpent'] = int(match.group(1).replace(',', ''))
