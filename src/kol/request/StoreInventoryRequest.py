import kol.Error as Error
from GenericRequest import GenericRequest
from kol.database import ItemDatabase
from kol.manager import PatternManager
from kol.util import StringUtils

class StoreInventoryRequest(GenericRequest):
        "This class is used to get a list of items currently in a user's store"

        def __init__(self, session):
                super(StoreInventoryRequest, self).__init__(session)
                self.url = session.serverURL + 'managestore.php'

	def parseResponse(self):
		"""
		Searches managestore.php for item name, quantity, price, limit, and ID.
		Returns the items with the usual keys in the item data base along with:

			quantity -- The number of the item in your mall store.
			   price -- The price of the item in your mall store.
			   limit -- The limit on the item in your mall store.
		"""
		storeInventoryPattern = PatternManager.getOrCompilePattern('storeInventory')

		items = []
		for match in storeInventoryPattern.finditer(self.responseText):
			name = match.group(1)
			if match.group(2) == None:
				quantity = 1
			else:
				quantity = int(match.group(2))
			price = int(match.group(3).replace(',',''))
			if match.group(4) == '<font size=1>(unlimited)</font>&nbsp;&nbsp;':
				limit = 0
			else:
				limit = int(match.group(4))
			itemID = int(match.group(5))
			item = ItemDatabase.getOrDiscoverItemFromId(itemID, self.session)
			item["quantity"] = quantity
			item["price"] = price
			item["limit"] = limit
			items.append(item)

		self.responseData["items"] = items
