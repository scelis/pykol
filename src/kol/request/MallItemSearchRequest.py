from GenericRequest import GenericRequest
from kol.database import ItemDatabase
from kol.manager import PatternManager

class MallItemSearchRequest(GenericRequest):
	"""
	Searches for an item at the mall. Note that stores from which you have already purchased
	the max that day will not appear.
	"""
	
	def __init__(self, session, itemName):
		super(MallItemSearchRequest, self).__init__(session)
		self.url = session.serverURL + 'searchmall.php'
		self.requestData['whichitem'] = itemName

	def parseResponse(self):
		items = []
		itemNoLimitPattern = PatternManager.getOrCompilePattern('mallItemSearchNoLimit')
		itemLimitPattern = PatternManager.getOrCompilePattern('mallItemSearchLimit')

		for match in itemNoLimitPattern.finditer(self.responseText):
			itemId = int(match.group(3))
			item = ItemDatabase.getItemFromId(descId, self.session)
			item["quantity"] = int(match.group(1))
			item["storeId"] = int(match.group(2))
			item["price"] = int(match.group(4))
			item["storeName"] = match.group(5).replace('<br>', ' ')
			items.append(item)

		for match in itemLimitPattern.finditer(self.responseText):
			itemId = int(match.group(4))
			item = ItemDatabase.getItemFromId(descId, self.session)
			item["quantity"] = int(match.group(1))
			item["limit"] = int(match.group(2))
			item["storeId"] = int(match.group(3))
			item["price"] = int(match.group(5))
			item["storeName"] = match.group(6).replace('<br>', ' ')
			items.append(item)

		self.responseData = items
